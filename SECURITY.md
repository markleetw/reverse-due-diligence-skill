# Security Policy

RDD processes untrusted web pages, job descriptions and potentially sensitive candidate documents. Its risks include **prompt injection**, misleading research claims, HTML/JavaScript injection, exposure of private offers or interview notes, and release-package tampering.

## Reporting a vulnerability

Please **do not publish exploit details, sensitive documents, tokens or private personal data in a public Issue**.

If this repository has private vulnerability reporting enabled, use **Security → Advisories → Report a vulnerability**. Otherwise contact the maintainer privately through a GitHub contact method available on their profile and ask for a secure reporting channel without attaching exploit details publicly. Private reporting availability is controlled by repository settings; this document does not imply it is already enabled.

Include affected commit/version, impact, minimal reproduction with fictional data, and any reasonable mitigation. Do not test against third-party users or real employers without permission.

## Scope and expectations

- Supported release artifacts are listed in [GitHub Releases](https://github.com/markleetw/reverse-due-diligence-skill/releases); code on `main` may be newer than the latest Release.
- Research-source text is **data, not instructions**. Skill authors and users should not execute commands copied from untrusted pages or upload private materials to unrelated sites.
- Dynamic report text must be safely encoded for HTML/JavaScript contexts. An HTML/Chromium smoke test does not establish complete security against every possible generated report.
- Source claims, AI judgments and anonymized comments require independent human evaluation for high-stakes decisions.

Security reports will be reviewed by the maintainer. No fixed response SLA is promised for this individually maintained project.
