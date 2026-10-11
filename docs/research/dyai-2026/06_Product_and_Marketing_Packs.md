# F. Drei Produkt-, Demo- und Marketing-Pakete
**11.10.2026 · Entwürfe, nicht veröffentlicht · keine Kunden-/Umsatzbehauptungen**

Quellen: eingefrorene Commits und Ausführungslogs in `02_Decision_and_Readiness.md`. Alle wirtschaftlichen Vorteile sind zu prüfende Hypothesen. Jeder Pitch unten umfasst weniger als 100 Wörter. Demo-Skripte beschreiben den engen überprüften Kern; bei PXAPI sind sie ausdrücklich ein **noch nicht ausgeführter Plan**.

# 1. Plumbline — One-Pager
**Headline:** Passing tests are not the whole story.
**Subline:** Check whether completion evidence meets explicit delivery requirements.

**Problemhypothese:** Agentisch erzeugte Software kann als fertig gemeldet werden, obwohl Nachweise eine relevante Anforderung nicht abdecken. **Käufer:** Engineering-/Platform-Leitung; spezifischer Budgethalter noch unbekannt.

**Produkt heute:** Repository-nahe Integrity-Prüfungen; lokal verifizierter deterministischer CLI-Kern mit positiver und negativer synthetischer Fixture. 77 Assertions bestanden. Ein optionaler Evidence-Manifest-Pfad ist kein universell aktives Sicherheitsnetz; ohne Manifest kann der betreffende Check passieren. Tokens/Dateireferenzen beweisen nicht automatisch tatsächliche Wirkung. Keine verifizierte Integration mit Agent Team oder ASM.

**Angebot:** Ein bezahlter, begrenzter Vergleich mit dem vorhandenen Reviewprozess. Ergebnis: Bericht über erkannte Nachweislücken, Fehlalarme, zusätzlichen Reviewaufwand und nicht abgedeckte Fälle. Nicht: fehlerfreie Software oder garantierte Einsparung.

**Differenzierungshypothese:** Eine explizite Anforderung-Nachweis-Regel direkt im Entwicklungsablauf. Gegen Braintrust, LangSmith und manuelles Review validieren. **Geschäftsmodellhypothese:** bezahlte Evaluation → wiederkehrende Team-/Repository-Nutzung mit Support. Preis und Zahlungsbereitschaft UNKNOWN.

**IP:** MIT-/claude-flow-Anteile sichtbar; vollständige Contributor-/Gesellschaftsrechte UNKNOWN. **Investment-Meilenstein:** unabhängiger Workflowvergleich plus mindestens ein belastbarer bezahlter Nutzungsfall, nicht weitere Repositories.

### Drei-Minuten-Demo
- **0:00–0:30:** Eine synthetische Anforderung und ihre geforderte Nachweisart zeigen. „Diese Fixture, keine Kundendaten.“
- **0:30–1:15:** `fake-only` über das CLI ausführen: Exit 3; präzise erklären, weshalb die Evidenzregel nicht erfüllt ist.
- **1:15–2:00:** Passende Integrations-Fixture: Exit 0. Nicht suggerieren, dass ein anderes reales System damit getestet wurde.
- **2:00–2:30:** Regel und Eingabedatei nebeneinander lesen; zeigen, was das Gate tatsächlich prüft und was nicht.
- **2:30–3:00:** Pilotfrage: Erkennt die Regel relevante Lücken besser als das bestehende Review, ohne unvertretbare Fehlalarme?

**Notwendige technische Maßnahmen (maximal drei):** Für diesen CLI-Kern keine Codeänderung erforderlich. **DEMO_BLOCKER:** keiner für den belegten Fixture-Pfad; reproduzierbare Umgebung und identische Inputs beibehalten. **MARKETING_BLOCKER:** manuelle Aktivierung/Opt-in und semantische Grenzen sichtbar machen. **RELEASE_BLOCKER:** Integrations-/Sicherheitsprüfung für reale Kundenumgebung. **DEFERRED:** vollständige autonome Delivery-Plattform.

### EN pitch
Plumbline is an early reliability framework for agentic software delivery. Its locally verified CLI checks whether supplied evidence satisfies explicit requirements. A passing test alone is not treated as proof of every intended outcome. We are seeking engineering teams for a paid evaluation on one bounded workflow, measuring missed evidence, false positives and review cost against their existing process. This is a narrow deterministic gate, not a guarantee of semantic correctness or an integrated autonomous development platform.

### DE pitch
Plumbline prüft, ob die vorgelegten Nachweise zu expliziten Anforderungen passen. Der enge CLI-Kern wurde lokal mit positiven und negativen synthetischen Fällen verifiziert. Wir suchen Engineering-Teams für eine begrenzte, bezahlte Evaluation gegenüber ihrem bisherigen Reviewprozess. Gemessen werden Nachweislücken, Fehlalarme und zusätzlicher Prüfaufwand. Noch nicht belegt sind Kundenwirkung, wiederkehrender Umsatz oder eine vollständige autonome Entwicklungsplattform. Unser Angebot ist ein überprüfbarer Einstieg, keine Garantie fehlerfreier Software.

### LinkedIn-Entwurf
Grüne Tests beantworten nicht automatisch jede Produktanforderung. Mit Plumbline untersuchen wir einen engen Ansatz: explizite Anforderungen an die Nachweise hinter einer Erledigungsbehauptung. Lokal funktionieren ein positiver und ein negativer synthetischer CLI-Fall. Noch offen ist der wirtschaftliche Nutzen im echten Reviewprozess. Wir suchen ein Engineering-Team für einen klar abgegrenzten Vergleich – einschließlich Fehlalarmen und zusätzlichem Aufwand. Keine autonome Plattform, kein garantierter ROI. Welche Nachweise fehlen euch heute am häufigsten bei AI-generierten Änderungen?

### Individueller Investor-Entwurf
An Gabriel Matuschka / Fly: „Your first-check focus on European technical founders is relevant to our deliberately narrow Plumbline evaluation. Could we qualify what evidence would distinguish a defensible reliability product from a feature? We can show a locally verified gate, but have not established customer ROI.“ Vollständiger Text und belegter Kontakt in Paket E.

### Separater Design-Partner-Entwurf — inovex
**Betreff:** Begrenzte Evaluation von Nachweisregeln im Agentic-Coding-Workflow

> Guten Tag, Ihr Agentic-Coding-Angebot ist der Anlass für eine konkrete Evaluationsfrage: Könnte ein expliziter Nachweis-Gate Ihre bestehenden Reviews sinnvoll ergänzen? Plumbline hat einen lokal verifizierten CLI-Kern; Kundenwirkung behaupten wir nicht. Wir schlagen einen bezahlten, eng begrenzten Vergleich auf einem freigegebenen Arbeitspaket vor. Bewertet würden Nachweislücken, Fehlalarme und Reviewaufwand. Wer verantwortet bei Ihnen solche Engineering-Evaluationen? Zunächst würden wir nur eine synthetische Demo zeigen, ohne Zugriff auf Kundencode.

# 2. ASM — One-Pager
**Headline:** Make product intent explicit before agents build.
**Subline:** A canonical product file, structured story mapping and human approval.

**Problemhypothese:** Ziele, Personas, Bedürfnisse und Entscheidungen gehen zwischen Discovery und Engineering verloren. **Käufer:** Head of Product, Product Ops oder Delivery-Leitung.

**Produkt heute:** Strukturiertes kanonisches Modell, Referenzvalidierung, explizite Freigabe, YAML-Persistenz und Export. 706 Tests bestanden. HTTP-Lesen, Freigeben, Exportieren und Ablehnung unbekannter Personas lokal verifiziert. Die lokale Seite lieferte HTML; eine echte Browser-End-to-End-Nutzung und reale Modellqualität wurden nicht überprüft. Keine automatische integrierte Umsetzung in Software behaupten.

**Angebot:** Eine Discovery-to-Engineering-Übergabe begleiten. Ergebnis: freigegebene Produktdatei und Vergleich, ob ein unabhängiger Reviewer Ziel, Persona, Anforderungen und offene Fragen korrekt rekonstruieren kann. **Nutzenhypothese:** weniger Kontextverlust; keine behauptete prozentuale Zeitersparnis.

**Wettbewerb:** Miro AI, Productboard und bestehende Dokument-/Workshop-Prozesse. Unterschied als Hypothese: kontrollierbare, portable Datei mit expliziten Referenzen und Freigabe. **Geschäftsmodell:** zunächst Design-Partnerschaft; später Team-/Workspace-Lizenz nur bei nachgewiesener wiederkehrender Nutzung. **IP:** fehlende Root-LICENSE und Rechtekette vor externer Verteilung klären.

### Drei-Minuten-Demo
- **0:00–0:30:** Kopierte öffentliche Produkt-Fixture zeigen; klar sagen: keine echten Kundendaten, kein aktiver KI-Provider.
- **0:30–1:15:** Kanonisches Modell per HTTP lesen, Beziehung von Ziel/Persona/Need/Story am tatsächlichen JSON erklären.
- **1:15–2:00:** Explizite synthetische Freigabe auslösen, Status lesen, YAML exportieren. Synthetischer Approver ist kein Authentifizierungsnachweis.
- **2:00–2:30:** Ein Modell mit gültig formatierter, aber unbekannter Persona einreichen; 422 `unknown_persona` zeigen. Syntaxfehler nicht mit Referenzvalidierung verwechseln.
- **2:30–3:00:** Export und Grenzen erklären: maschinenlesbarer Produktkontext, noch kein autonomer Discovery-/Delivery-Kreislauf.

**Notwendige technische Maßnahmen (maximal drei):** Keine Codeänderung für den belegten HTTP-Pfad. Für eine ausdrücklich interaktive Browser-Demo zuerst deren Bedienpfad separat testen; dies ist eine Verifikation, kein geforderter Vollausbau. **DEMO_BLOCKER:** nur für Live-KI-Claims fehlt ein realer Provider-/Outputnachweis. **MARKETING_BLOCKER:** lokale HTTP-Verifikation nicht als Browser-/Live-KI-Erfolg darstellen. **RELEASE_BLOCKER:** echte Authentifizierung, Zugriffsschutz und Mandantengrenzen vor Kundendaten. **DEFERRED:** Jira-Bidirektionalität, Multiplayer und Agent-Delivery-Integration.

### EN pitch
ASM is an early story-mapping tool built around a canonical, agent-readable product file. It connects goals, personas, needs and explicit human approval. Its tests pass locally, and we verified the read, approve and export workflow through HTTP. Live AI quality and customer outcomes remain unverified. We are seeking a product team to evaluate one discovery-to-engineering handoff: can a reviewer recover the original intent and identify missing requirements more reliably? The immediate offer is a scoped design partnership, not an autonomous product team.

### DE pitch
ASM hält Ziele, Personas, Bedürfnisse und Stories in einer kanonischen Produktdatei zusammen. Explizite menschliche Freigabe und Referenzvalidierung sind Teil des bestehenden Codes; Lesen, Freigeben und Export wurden lokal per HTTP verifiziert. Wir suchen ein Produktteam für eine abgegrenzte Discovery-to-Engineering-Übergabe. Der Test: Kann ein unabhängiger Reviewer die ursprüngliche Absicht und fehlende Anforderungen besser erkennen? Live-KI-Qualität und Kundenwirkung sind noch offen. ASM ist heute kein autonomes Produktteam und keine fertige Enterprise-Collaboration-Suite.

### LinkedIn-Entwurf
Der schwierigste Teil einer Übergabe ist oft nicht das Dokument, sondern die verlorene Absicht. ASM untersucht einen kleinen Gegenentwurf: strukturierte Produktziele, Personas, Bedürfnisse und Stories in einer kanonischen Datei – mit expliziter menschlicher Freigabe. Der lokale HTTP-Kern ist verifiziert; Live-KI-Qualität und wirtschaftlicher Nutzen sind es noch nicht. Wir suchen ein Produktteam für genau eine Übergabe als Design-Partnerschaft. Nicht „mehr KI“, sondern eine prüfbare Frage: Versteht die nächste Person, warum etwas gebaut werden soll?

### Individueller Investor-Entwurf — Seedcamp / Sia Houchangnia
**Subject:** Human-approved product context — an early ASM fit check

> Hello Sia, Seedcamp’s Topograph investment drew our attention to your interest in structured, evidence-grounded infrastructure. ASM addresses a different problem: preserving product intent in a canonical, human-approved file. We verified reading, approval and export locally through HTTP, but have not established customer outcomes or live AI quality. Would you help us qualify whether this early product-context thesis fits Seedcamp? Our next milestone is one measured discovery-to-engineering handoff, not a claim of autonomous delivery.

Route: [Seedcamp-Pitchformular](https://seedcamp.typeform.com/to/pMlqt8). Bezug: [Topograph-Mitteilung 20.03.2026](https://seedcamp.com/views/seedcamp-leads-topographs-e2m-seed-to-fix-the-broken-infrastructure-behind-global-kyb/). Kein direkter PM-Mandatsbeweis.

### Separater Design-Partner-Entwurf — iteratec
**Betreff:** Eine Discovery-Übergabe mit freigegebener Produktdatei evaluieren

> Guten Tag, für Ihre Product-/Delivery-Arbeit möchten wir einen begrenzten Design-Partner-Test vorschlagen. ASM hält Produktkontext in einer strukturierten Datei; Freigabe und Export sind lokal verifiziert. Könnten wir an einer anonymisierbaren Übergabe prüfen, ob ein unabhängiger Reviewer die ursprünglichen Ziele und Anforderungen nachvollziehen kann? Scope, Abnahme und eine mögliche Vergütung würden wir vorab vereinbaren. Es geht nicht um einen Plattformwechsel oder um autonome Discovery. Wer wäre bei Ihnen für diese Problemstellung zuständig?

# 3. PXAPI — One-Pager
**Headline:** A finding should come with its evidence.
**Subline:** Static website diagnosis that keeps failed measurements separate from observed issues.

**Problemhypothese:** Agenturen verbringen Zeit damit, automatisierte Befunde zu verifizieren und ihren Kunden verständlich zu belegen. **Käufer:** Digital-/SEO-/Experience-Agentur, Website-Verantwortliche.

**Produkt heute:** Code für statische Homepage-Analyse und eine Finding→Evidence→Measurement-Kette. Unknown, absent und not-applicable sind nicht austauschbar. Findings benötigen bekannte Evidenz derselben Ausführung. **CODE_EVIDENCE_ONLY**: Tests und End-to-End-Ausführung in dieser Umgebung nicht durchgeführt. Python ≥3.13 fehlt; Interpreter-Download scheiterte an TLS. Keine fertige Pixelkiez-Oberfläche, kein deployter Diagnose-Agent aus separatem Repo abgeleitet.

**Bedingtes Angebot:** Nach erfolgreicher Laufzeitprüfung ein begrenzter, autorisierter Homepage-Audit mit nachvollziehbarem Bericht. **Nicht verkaufen:** laufende Produktions-API, garantierte Such-/KI-Sichtbarkeit, Conversion-Steigerung oder umfassende Rechts-/Accessibility-Konformität.

**Alternativen:** Screaming Frog, Lighthouse, manuelle Agenturprüfung. **Differenzierungshypothese:** explizite Belegbarkeit und Unknown-Semantik reduzieren Nachprüfung. **Geschäftsmodellentscheidung:** zunächst technologiegestützter Service; Lizenz/API erst bei standardisierten wiederkehrenden Aufträgen. **VC-Fit:** derzeit schwächer als bei Plumbline/ASM. Rechtekette trotz MIT UNKNOWN.

### Drei-Minuten-Demo — PLAN, noch nicht ausgeführt
- **0:00–0:30:** Scope erläutern: eine autorisierte statische Homepage, kein vollständiger Website-Crawl.
- **0:30–1:15:** Analyse mit kompatibler Laufzeit starten. Nur tatsächlichen Output zeigen; bei Fehler abbrechen und Fehler benennen.
- **1:15–2:00:** Einen tatsächlich erzeugten Befund bis zur Messung derselben Ausführung zurückverfolgen. Keine Muster-JSON als Laufzeitoutput ausgeben.
- **2:00–2:30:** Kontrollierten Messfehler prüfen: Ergebnis unbekannt, nicht automatisch Website-Mangel. Dies ist erst nach Ausführung als verifiziert zu bezeichnen.
- **2:30–3:00:** Agentur-Reviewer bewertet Nutzbarkeit und Nachprüfaufwand. Keine Wirkungs-/Umsatzfolie.

**Notwendige technische Maßnahmen (zwei):** (1) kompatible Python-Laufzeit sicher bereitstellen; keine TLS-Prüfung abschalten. (2) Dependencies/Tests und einen autorisierten Positiv-/Fehlerfall ausführen und protokollieren. **DEMO_BLOCKER:** beide Schritte offen. **MARKETING_BLOCKER:** CODE_EVIDENCE_ONLY sichtbar lassen. **RELEASE_BLOCKER:** Eingabe-/Netzwerkschutz, Datenschutz und Betriebsverantwortung vor öffentlichem API-Betrieb prüfen. **DEFERRED:** JS-Rendering, komplette Website-Crawls, Billing und Multi-Tenant-SaaS, sofern nicht Pilotanforderung.

### EN pitch
PXAPI is an early website-analysis engine that links findings to evidence and measurements. Its code distinguishes an observed issue from a failed measurement, so a timeout should not become a negative verdict about a business. We are seeking an agency partner for a bounded evaluation of static-page diagnosis. A compatible runtime is still needed before the local demo can be verified. We make no production or conversion-impact claim. The commercial question is whether evidence-backed reports reduce manual verification enough to support repeatable paid delivery.

### DE pitch
PXAPI verknüpft Website-Befunde mit Evidenz und Messungen. Der Code trennt beobachtete Probleme von fehlgeschlagenen Messungen: Ein Timeout darf nicht automatisch zum negativen Unternehmensurteil werden. Wir suchen eine Agentur für eine begrenzte Evaluation statischer Homepage-Diagnosen. Die lokale Laufzeitprüfung steht noch aus; eine fertige Produktions-API oder Conversion-Wirkung behaupten wir nicht. Zunächst soll sich zeigen, ob die nachvollziehbaren Berichte manuelle Nachprüfung verringern und wiederholbare bezahlte Aufträge ermöglichen.

### LinkedIn-Entwurf
„Nicht messbar“ ist nicht dasselbe wie „schlecht“. PXAPI untersucht diese Unterscheidung in der Website-Diagnose: Befunde sollen auf Evidenz und konkrete Messungen zurückführen. Der Code ist geprüft, die lokale Ausführung wegen einer Laufzeitabhängigkeit noch nicht verifiziert. Wir suchen eine Agentur, die nach dieser Prüfung einen begrenzten Diagnosefall mit uns bewertet. Die Frage ist nicht, ob ein weiterer Scan möglich ist, sondern ob belegbare Ergebnisse die manuelle Nachprüfung tatsächlich erleichtern. Kein versprochener SEO- oder Conversion-Uplift.

### Individueller Investor-Entwurf — Tiny / Philipp Moehring, bewusst zurückgestellt
**Subject:** Service-first website diagnostics — qualifying whether equity is appropriate

> Hello Philipp, Tiny’s European pre-seed focus makes your perspective relevant to a financing question, not a ready fundraising claim. PXAPI links static website findings to their measurements. The code is reviewed, but local execution and paid demand remain unverified. We currently see a service-first evaluation rather than a proven venture-scale API. After a paid agency pilot, would this fit your scope, or would customer-funded development be more appropriate? We would not propose an equity round before clarifying repeatability and capital need.

Kontakt: hello@tiny.vc laut [offizieller Seite](https://tiny.vc/). **Nicht priorisiert:** Register-Tiny-Score gilt ASM, nicht PXAPI. Dieses Anschreiben ist bewusst nur ein späterer, individuell adressierter Qualifikationsentwurf; kein belegter PXAPI-Investor-Fit.

### Separater Design-Partner-Entwurf — Valtech, erst nach Runtime-Nachweis
**Betreff:** Nachvollziehbare Homepage-Befunde in einem begrenzten Agentur-Pilot

> Guten Tag, für Ihre Experience-/Commerce-Arbeit möchten wir einen kleinen Vergleich vorschlagen: Sind Website-Befunde leichter nutzbar, wenn jede Aussage bis zur konkreten Messung nachvollziehbar ist? PXAPI implementiert diese Evidenzkette für statische Homepage-Diagnosen. Derzeit fehlt uns noch der lokale Laufzeitnachweis; erst danach würden wir einen bezahlten Pilot anbieten. Wäre die Problemstellung für Ihre Audit-Verantwortlichen grundsätzlich relevant? Keine Conversion-Versprechen, kein vollständiger Website-Crawl und kein Zugriff auf Kundensysteme ohne ausdrückliche Freigabe.

# Gemeinsame Go-/No-Go-Regel
Ein Pitch darf vor Prüfung Interesse qualifizieren, aber keine nicht verifizierte Lieferung zusagen. Eine Pilotzusage benötigt Scope, Rechte, Verantwortliche, verfügbare Kapazität und Abnahmekriterien. Ein Investment-Pitch benötigt zusätzlich rechtliche Entität, vollständige Rechtekette und belastbaren Mittelverwendungsplan. Für keines der drei Angebote liegt unabhängiger Kunden-/Umsatzbeweis vor.
