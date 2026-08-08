"""Interface de linha de comando do OSINT Local."""

from pathlib import Path
from typing import Annotated

import typer

from osint_local.analyzers.file_integrity import compare_files
from osint_local.analyzers.username_search import search_username
from osint_local.collectors.company.brasilapi import (
    search_company_by_cnpj,
)
from osint_local.collectors.image_metadata import analyze_image
from osint_local.collectors.mastodon_username import (
    search_mastodon_username,
)
from osint_local.errors import (
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
from osint_local.errors.handlers import format_operator_error
from osint_local.presenters.company_summary import (
    format_company_result,
)
from osint_local.presenters.hash_summary import format_hash_comparison
from osint_local.presenters.photo_summary import format_photo_metadata
from osint_local.presenters.username_summary import (
    format_username_results,
)
from osint_local.ui.console import (
    format_field,
    format_footer,
    format_header,
    format_paragraph,
    format_section,
)
from osint_local.ui.formatters import format_command
from osint_local.version import (
    APP_NAME,
    AUTHOR,
    DESCRIPTION,
    VERSION,
)


app = typer.Typer(
    name="osint-local",
    add_completion=False,
    no_args_is_help=False,
    context_settings={
        "help_option_names": [],
    },
)


def format_main_help() -> str:
    """Retorna a ajuda principal em português."""

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
            "procurar-usuario <username>",
            "Pesquisa um identificador nas fontes públicas registradas.",
        ),
        format_command(
            "procurar-mastodon <usuario@instancia>",
            "Verifica uma conta Mastodon pelo identificador federado.",
        ),
        format_command(
            "consultar-cnpj <cnpj>",
            "Consulta informações públicas de uma empresa pelo CNPJ.",
        ),
    ]

    examples = [
        "osint-local analisar-imagem foto.jpg",
        (
            "osint-local comparar-arquivos "
            "foto_original.jpg foto_analisada.jpg"
        ),
        "osint-local procurar-usuario FB-001",
        "osint-local procurar-mastodon gargron@mastodon.social",
        "osint-local consultar-cnpj 60701190000104",
    ]

    lines = [
        format_header(APP_NAME),
        "",
        format_paragraph(DESCRIPTION),
        "",
        format_paragraph(
            "Desenvolvida para auxiliar o operador na coleta, "
            "organização e correlação de informações. "
            "O sistema não substitui o julgamento do operador."
        ),
        "",
        format_section("Comandos disponíveis"),
        "",
        "\n\n".join(commands),
        "",
        format_section("Exemplos"),
        "",
        "\n\n".join(examples),
        "",
        format_section("Ajuda"),
        "",
        "osint-local --ajuda",
        "osint-local -h",
        "",
        format_footer(),
    ]

    return "\n".join(lines)


@app.callback(invoke_without_command=True)
def root(
    context: typer.Context,
    ajuda: Annotated[
        bool,
        typer.Option(
            "--ajuda",
            "-h",
            help="Exibe a ajuda principal e encerra.",
            is_eager=True,
        ),
    ] = False,
) -> None:
    """Controla a entrada principal da aplicação."""

    if ajuda or context.invoked_subcommand is None:
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


@app.command("procurar-usuario")
def search_username_command(
    username: Annotated[
        str,
        typer.Argument(
            metavar="USERNAME",
        ),
    ],
) -> None:
    """Pesquisa um username em múltiplas fontes públicas."""

    normalized_username = username.strip()

    if not normalized_username:
        print(
            format_operator_error(
                "O nome de usuário não pode estar vazio.",
                guidance=(
                    "Informe um identificador válido e tente novamente."
                ),
            )
        )
        raise typer.Exit(code=1)

    results = search_username(normalized_username)

    print(
        format_username_results(
            normalized_username,
            results,
        )
    )


@app.command("procurar-mastodon")
def search_mastodon_command(
    handle: Annotated[
        str,
        typer.Argument(
            metavar="USUARIO@INSTANCIA",
        ),
    ],
) -> None:
    """Verifica uma conta Mastodon pelo identificador federado."""

    result = search_mastodon_username(handle)

    print(
        format_username_results(
            result.username,
            [result],
        )
    )


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


def main() -> None:
    """Executa a aplicação de linha de comando."""

    app()
