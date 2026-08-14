"""Interface de linha de comando do PERSPICIO."""

from pathlib import Path
from typing import Annotated

import typer

from perspicio.analyzers.file_integrity import compare_files
from perspicio.collectors.company.brasilapi import (
    search_company_by_cnpj,
)
from perspicio.collectors.image.metadata import analyze_image
from perspicio.errors import (
    CompanyNetworkError,
    CompanyNotFoundError,
    CompanyServiceError,
    HashCalculationError,
    HashFileNotFoundError,
    HashPermissionError,
    ImageFileNotFoundError,
    ImagePermissionError,
    InvalidImageError,
)
from perspicio.errors.handlers import format_operator_error
from perspicio.presenters.company_summary import (
    format_company_result,
)
from perspicio.presenters.hash_summary import format_hash_comparison
from perspicio.presenters.photo_summary import format_photo_metadata
from perspicio.ui.console import (
    format_field,
    format_footer,
    format_header,
    format_paragraph,
    format_section,
)
from perspicio.ui.formatters import format_command
from perspicio.version import (
    APP_NAME,
    AUTHOR,
    DESCRIPTION,
    VERSION,
)

from perspicio.analysis.propaganda.ai.adapter import ai_result_to_draft
from perspicio.analysis.propaganda.ai.context import build_ai_context
from perspicio.analysis.propaganda.ai.mock import MockPropagandaAI
from perspicio.analysis.propaganda.analyzer import analyze_propaganda
from perspicio.analysis.propaganda.review import (
    apply_validated_draft,
    review_analysis_suggestion,
    review_ocr_texts,
    review_visual_elements,
)
from perspicio.analysis.propaganda.vision.rules import generate_suggestions
from perspicio.presenters.propaganda_summary import (
    format_propaganda_analysis,
)


app = typer.Typer(
    name="perspicio",
    add_completion=False,
    no_args_is_help=False,
    context_settings={
        "help_option_names": [],
    },
)


def format_main_help() -> str:
    """Retorna a tela principal do PERSPICIO."""

    commands = [
        format_command(
            "informacoes",
            "Exibe informações sobre a aplicação.",
        ),
        format_command(
            "analisar-imagem <arquivo>",
            "Analisa metadados técnicos e EXIF de uma imagem.",
        ),
        format_command(
            "comparar-arquivos <arquivo_a> <arquivo_b>",
            "Compara dois arquivos utilizando SHA-256.",
        ),
        format_command(
            "consultar-cnpj <cnpj>",
            "Consulta informações públicas de uma empresa pelo CNPJ.",
        ),
        format_command(
            "analisar-propaganda <arquivo>",
            "Analisa uma peça de propaganda e apoia a aplicação do método OCAVE.",
        ),
    ]

    lines = [
        format_header(APP_NAME),
        "",
        format_paragraph(DESCRIPTION),
        "",
        format_paragraph(
            "Desenvolvida para auxiliar o operador na coleta, "
            "organização e análise de informações. "
            "O sistema não substitui o julgamento do operador."
        ),
        "",
        format_section("Comandos disponíveis"),
        "",
        "\n\n".join(commands),
        "",
        format_footer(),
    ]

    return "\n".join(lines)


@app.callback(invoke_without_command=True)
def root(
    context: typer.Context,
) -> None:
    """Controla a entrada principal da aplicação."""

    if context.invoked_subcommand is None:
        print(format_main_help())
        raise typer.Exit()


@app.command("informacoes")
def show_information() -> None:
    """Exibe informações sobre a aplicação."""

    lines = [
        format_header(APP_NAME),
        "",
        format_section("Informações da aplicação"),
        "",
        format_field("Versão", VERSION),
        format_field("Autor", AUTHOR),
        format_field("Licença", "MIT"),
        "",
        "Descrição:",
        "",
        format_paragraph(DESCRIPTION, indent=4),
        "",
        format_footer(),
    ]

    print("\n".join(lines))


@app.command("analisar-imagem")
def analyze_image_command(
    file_path: Annotated[
        Path,
        typer.Argument(
            exists=False,
            file_okay=True,
            dir_okay=False,
            readable=False,
            metavar="ARQUIVO",
        ),
    ],
) -> None:
    """Analisa os metadados de uma imagem."""

    try:
        metadata = analyze_image(file_path)
        print(format_photo_metadata(metadata))

    except ImageFileNotFoundError as error:
        print(
            format_operator_error(
                "Arquivo de imagem não encontrado.",
                path=error.file_path,
                guidance="Verifique o caminho e tente novamente.",
            )
        )
        raise typer.Exit(code=1)

    except InvalidImageError as error:
        print(
            format_operator_error(
                "O arquivo informado não é uma imagem reconhecida.",
                path=error.file_path,
                guidance=(
                    "Utilize uma imagem válida, como JPEG, PNG ou TIFF."
                ),
            )
        )
        raise typer.Exit(code=1)

    except ImagePermissionError as error:
        print(
            format_operator_error(
                "Sem permissão para ler a imagem.",
                path=error.file_path,
                guidance="Verifique as permissões do arquivo.",
            )
        )
        raise typer.Exit(code=1)


@app.command("comparar-arquivos")
def compare_files_command(
    first_file: Annotated[
        Path,
        typer.Argument(
            exists=False,
            file_okay=True,
            dir_okay=False,
            readable=False,
            metavar="ARQUIVO_A",
        ),
    ],
    second_file: Annotated[
        Path,
        typer.Argument(
            exists=False,
            file_okay=True,
            dir_okay=False,
            readable=False,
            metavar="ARQUIVO_B",
        ),
    ],
) -> None:
    """Compara a integridade de dois arquivos."""

    try:
        comparison = compare_files(first_file, second_file)
        print(format_hash_comparison(comparison))

    except HashFileNotFoundError as error:
        print(
            format_operator_error(
                "Arquivo não encontrado para comparação.",
                path=error.file_path,
                guidance="Verifique o caminho e tente novamente.",
            )
        )
        raise typer.Exit(code=1)

    except HashPermissionError as error:
        print(
            format_operator_error(
                "Sem permissão para ler o arquivo.",
                path=error.file_path,
                guidance="Verifique as permissões do arquivo.",
            )
        )
        raise typer.Exit(code=1)

    except HashCalculationError as error:
        print(
            format_operator_error(
                "Não foi possível calcular o hash do arquivo.",
                path=error.file_path,
                guidance=(
                    "Confirme que o caminho aponta para um arquivo legível."
                ),
            )
        )
        raise typer.Exit(code=1)


@app.command("consultar-cnpj")
def search_cnpj_command(
    cnpj: Annotated[
        str,
        typer.Argument(
            metavar="CNPJ",
        ),
    ],
) -> None:
    """Consulta informações públicas de uma empresa."""

    try:
        company = search_company_by_cnpj(cnpj)
        print(format_company_result(company))

    except ValueError:
        print(
            format_operator_error(
                "O CNPJ informado é inválido.",
                guidance=(
                    "Informe um CNPJ com 14 dígitos "
                    "e tente novamente."
                ),
            )
        )
        raise typer.Exit(code=1)

    except CompanyNotFoundError:
        print(
            format_operator_error(
                "O CNPJ informado não foi localizado.",
                guidance=(
                    "Confirme o número informado "
                    "e tente novamente."
                ),
            )
        )
        raise typer.Exit(code=1)

    except CompanyNetworkError:
        print(
            format_operator_error(
                "Não foi possível acessar a fonte de consulta.",
                guidance=(
                    "Verifique sua conexão com a internet "
                    "e tente novamente."
                ),
            )
        )
        raise typer.Exit(code=1)

    except CompanyServiceError:
        print(
            format_operator_error(
                "A fonte de consulta apresentou uma falha.",
                guidance="Tente novamente mais tarde.",
            )
        )
        raise typer.Exit(code=1)


@app.command("analisar-propaganda")
def analyze_propaganda_command(
    file_path: Annotated[
        Path,
        typer.Argument(
            exists=False,
            file_okay=True,
            dir_okay=False,
            readable=False,
            metavar="ARQUIVO",
        ),
    ],
) -> None:
    """Analisa uma peça de propaganda."""

    try:
        analysis = analyze_propaganda(file_path)

        analysis.observed.texts = review_ocr_texts(
            analysis.observed.ocr_texts
        )

        review_visual_elements(
            analysis.observed.visual_elements
        )

        draft = generate_suggestions(
            analysis.observed
        )

        review_analysis_suggestion(
            "Frase-síntese",
            draft.slogan,
        )

        analysis = apply_validated_draft(
            analysis,
            draft,
        )

        ai_context = build_ai_context(
            analysis
        )

        ai = MockPropagandaAI()

        ai_result = ai.analyze(
            ai_context
        )

        ai_draft = ai_result_to_draft(
            ai_result
        )

        review_analysis_suggestion(
            "Ideia-força",
            ai_draft.force_idea,
        )

        analysis = apply_validated_draft(
            analysis,
            ai_draft,
        )

        print(format_propaganda_analysis(analysis))

    except FileNotFoundError:
        print(
            format_operator_error(
                "Arquivo de propaganda não encontrado.",
                path=file_path,
                guidance="Verifique o caminho e tente novamente.",
            )
        )
        raise typer.Exit(code=1)

    except ValueError as error:
        print(
            format_operator_error(
                str(error),
                path=file_path,
                guidance=(
                    "Utilize uma imagem válida nos formatos "
                    "JPEG, PNG ou WEBP."
                ),
            )
        )
        raise typer.Exit(code=1)


def main() -> None:
    """Executa a aplicação de linha de comando."""

    app()
