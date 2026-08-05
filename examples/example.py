from osint_local.presenters.case_summary import format_investigation
from datetime import datetime

from osint_local.models.evidence import Evidence
from osint_local.models.investigation import Investigation
from osint_local.models.target import Target


case = Investigation(
    name="CASO-001",
    analyst="Fábio",
    description="Primeiro caso de teste.",
)

target = Target(
    full_name="Pessoa de teste",
    phone_numbers=["(21) 99999-0000"],
    emails=["teste@example.com"],
)

evidence = Evidence(
    evidence_type="photo",
    source="Arquivo local",
    description="Fotografia utilizada apenas para teste.",
    collected_at=datetime.now(),
)

case.add_target(target)
case.add_evidence(evidence)

print(format_investigation(case))
