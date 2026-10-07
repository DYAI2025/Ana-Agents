# Connector & Permission Policy

Status: ACTIVE DISTRIBUTION CONTRACT

## Principle

The Agent may orchestrate installed skills and approved runtime/CRM capabilities. Capability existence never grants authority.

## Allowed by default

- read lead identity and already-authorized CRM context;
- invoke `ana-brand-intel`;
- invoke `ana-outreach-compose`;
- read approved creator/project knowledge;
- return structured analysis and drafts for human review.

## Not allowed by default

- CRM create/update/delete;
- bulk export of CRM/contact data;
- MAIL_SEND;
- issuing or fabricating SendPermission;
- changing suppression, DNC, opt-out, duplicate, approval, or compliance state;
- publishing or broadly sharing the Agent;
- adding credentials/secrets to prompts or repository files.

## Write/send activation

A connector write or send capability may be enabled only when all of the following are true:

1. the exact connector/runtime is identified;
2. the requested scope is explicitly authorized by a human;
3. deterministic policy gates exist for that action;
4. the action has read-after-write or receipt evidence;
5. the skill itself still cannot self-grant the authority.

## Vince CRM orchestrator binding

The repository currently describes an external Vince CRM orchestrator but does not contain or identify its authoritative Ana-specific implementation artifact.

State: `MISSING`.

Until that artifact is identified, integration verification may test only the Agent/skill boundary contract, not claim that Vince's production orchestrator is integrated.
