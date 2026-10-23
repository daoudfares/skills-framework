---
name: mulesoft-developer
description: Build, review, debug and test Mule 4 applications for MuleSoft integrations. Use when working with Mule configuration XML, flows, connectors, routers and scopes, error handlers, mule-artifact.json or a Mule pom.xml, when writing or fixing MUnit tests, when a Mule app fails to deploy or raises a runtime error, or when asked about Anypoint Code Builder, packaging, streaming, batch jobs or transactions. For the DataWeave expressions inside a Mule app, use the dataweave-developer skill.
---

# MuleSoft Developer

Mule 4 applications are XML. A flow declares a sequence of components that
process one immutable Mule event, and everything else — connectors, error
handlers, transactions — configures that. This skill covers writing that XML,
choosing the right component, testing it with MUnit, and reading the errors the
runtime actually produces.

Documentation here reflects **Mule runtime 4.12** and **MUnit 3.7**. Check the
runtime a project targets before relying on a recent feature: `minMuleVersion`
in `mule-artifact.json` states what the app requires.

## DataWeave is a separate skill

Every `#[...]` expression, every Transform Message component and every `.dwl`
file is DataWeave. **Use the `dataweave-developer` skill for the expression
language itself** — its functions, selectors, type system and formats. This
skill covers where expressions attach to Mule, not what goes inside them.

## Application anatomy

```text
my-app/
├── pom.xml                    dependencies (connectors carry classifier mule-plugin)
├── mule-artifact.json         name, minMuleVersion, requiredProduct, configs, secureProperties
└── src/
    ├── main/mule/             flow configuration XML   (mandatory)
    ├── main/resources/        properties, .dwl files, schemas
    └── test/munit/            MUnit suites
```

`pom.xml`, `mule-artifact.json` and `src` are all mandatory; nothing else in the
root is packaged. A connector's XML namespace only resolves if its dependency is
declared — schemas are generated per artifact from the declared dependencies, so
`schemaLocation` and `pom.xml` must agree.

`mvn clean package` produces the deployable JAR; `mvn clean test` runs MUnit.

## Finding the right reference

Read only the file you need; they are large.

| Need | Read |
|---|---|
| XML for a Core component: attributes, child elements, skeleton | `references/components.md` |
| Mule event, message, payload/attributes/variables, flows vs subflows, sources | `references/flows.md` |
| Choice, Scatter-Gather, Round Robin, First Successful, For Each, Until Successful, Async, Try, Cache | `references/routers.md` |
| Error types and hierarchy, On-Error components, mappings, Raise Error | `references/errors.md` |
| `mule-artifact.json`, config XML, properties, secure properties, global elements, domains | `references/configuration.md` |
| Repeatable streams, buffer sizing, streaming strategies | `references/streaming.md` |
| Batch Job, Batch Step, Batch Aggregator, batch error handling | `references/batch.md` |
| Transactions, XA, reconnection, redelivery, object stores, reliability patterns | `references/reliability.md` |
| Maven plugin, packaging, CloudHub 2.0, Runtime Fabric, on-premises | `references/deployment.md` |
| Back-pressure, `maxConcurrency`, pooling, execution engine, tuning | `references/performance.md` |
| TLS, OAuth grant types, Spring Security, LDAP | `references/security.md` |
| Log4j2 config, MDC, verbose logging, stack traces, notifications | `references/logging.md` |
| MUnit suites, tests, before/after, parameterization, coverage | `references/munit.md` |
| Mock When, Verify Call, Spy, Set Event, assertions, storage and queue processors | `references/munit-processors.md` |
| `MunitTools::` matchers | `references/munit-matchers.md` |
| Worked MUnit examples — mocking errors, files, schedulers, DB and FTP servers | `references/munit-cookbook.md` |
| Anypoint Code Builder commands, local runtime, launch arguments, built-in connectors | `references/acb.md` |
| An error or deployment failure you do not recognise | `references/troubleshooting.md` |

## Things that are easy to get wrong

**The event is immutable.** Every processor returns a new one. `payload`,
`attributes` and `vars` are what you read; there is no assignment.

**Attributes belong to the last message produced.** An HTTP request overwrites
`attributes` with the response's. Capture what you need into a variable before
the call, not after.

**`flow-ref` into a subflow is inlining, not calling.** The subflow's contents
are copied into every call site, so anything needing a unique instance breaks —
a Batch Job inside a subflow referenced twice fails the app at deployment.
Subflows also have no error handler. Use a flow when you want either.

**Handler order decides the match.** On-Error components are evaluated top to
bottom; a `type="ANY"` above a specific type swallows everything below it.

**On Error Continue marks the owner successful.** It commits transactions and
returns its result as the flow's result. On Error Propagate rolls back and
rethrows. Choosing the wrong one silently turns a failure into a 200.

**`CRITICAL` and source errors cannot be handled.** `OVERLOAD`,
`FLOW_BACK_PRESSURE`, `FATAL_JVM_ERROR`, and everything under `SOURCE` and
`SOURCE_RESPONSE`, are logged, not caught. `ANY` does not match them.

**Two failures from two connectors look identical.** Two HTTP requests both
raise `HTTP:CONNECTIVITY`. Add `<error-mapping>` per operation to tell them
apart.

**For Each does not change the payload.** Its output is its input. Results have
to be accumulated into a variable, or the scope replaced with something that
aggregates.

**Parallel For Each buffers every result.** It runs out of memory on large
collections; Batch Job is the construct for those.

**Scatter-Gather returns a map, not a list** — `{0: msg0, 1: msg1, ...}` — and
needs at least two routes or the app will not start.

**Streams are repeatable by default, and that is load-bearing.** Scatter-Gather
and Cache do not work with non-repeatable streams. The default file-store
strategy buffers 512 KB in memory before spilling to disk.

**Several defaults are Enterprise-only**: file-stored streaming, Batch, the
Transform Message component, MUnit coverage. Check `requiredProduct`.

**MUnit does not start event sources.** An HTTP listener stays dormant unless
the test declares `munit:enable-flow-sources`. Most tests should call the flow
with `flow-ref` instead.

**A multi-line script in an XML attribute becomes one line.** XML parsers
normalise line breaks inside attribute values to spaces, so
`value="#[%dw 2.0 ⏎ output application/java ⏎ ---…]"` reaches DataWeave with
its header on a single line. Write anything longer than an expression in an
element that takes CDATA — `ee:transform` with `ee:set-variable` or
`ee:set-payload`, or a connector's body element — or encode the breaks as
`&#xA;`.

**Connector attributes can be undocumented.** Some connectors type their
source attributes only as `Object` (Google Pub/Sub is one). Read every field in
one place, log `attributes` at DEBUG on a first real run, and correct the paths
there rather than trusting a guessed name across flows.

## Which layer owns which contract

API-led layering only pays off if each layer exposes its own contract. The
boundary between two contracts is where a mapping belongs, and nowhere else.

| Layer | Exposes | Changes when |
|---|---|---|
| System | The source system's contract, mirrored — its resources, its field names, its values | The source system changes |
| Process | The organisation's canonical contract for a business domain | The domain model changes |
| Experience | One consumer's contract | That consumer asks for something |

- **A System API never speaks the canonical vocabulary.** Renaming a source
  field inside a System API hides the source system from the Process layer and
  turns that application into a second Process API. Protocol, credentials,
  pagination and error mapping are a System API's job; vocabulary is not.
- **The Process layer is where a source system disappears.** Replacing it then
  means rewriting one mapping, with nothing above affected. A canonical field
  no system supplies is `null`, not absent: the contract describes the domain,
  not today's sources.
- **An Experience API maps the canonical contract onto its consumer.** When a
  consumer imposes nothing, its contract may be a copy of the canonical one and
  the mapping the identity — keep it a separate contract anyway, so the first
  consumer-specific demand does not reach down a layer.
- **An Experience API calling a System API** inherits the source system's
  vocabulary, which is what the Process layer exists to absorb. If a shortcut is
  taken deliberately, write down why, next to the code.

## Sharing configuration between applications

Flows, sub-flows and error handlers can be shared as a library: a Mule
application packaged as a plugin, added as a dependency and imported.

```xml
<!-- library pom.xml: mule-maven-plugin -->
<configuration>
  <classifier>mule-plugin</classifier>
</configuration>
```

```json
// library mule-artifact.json: without this, the application cannot see the file
"classLoaderModelLoaderDescriptor": {
  "id": "mule",
  "attributes": { "exportedResources": ["my-common-errors.xml"] }
}
```

```xml
<!-- application: dependency with <classifier>mule-plugin</classifier>, then -->
<import file="my-common-errors.xml" />
```

- **Name imported files uniquely** — they share one classpath with the
  application's own configuration files.
- **Connectors the library uses are compile-scope dependencies.** With
  `provided`, packaging fails with `Can't resolve …/mule-<connector>.xsd`: the
  build validates the XML against the schemas of compile dependencies only.
- **The library does not own global elements the application defines.** Refer
  to a connector configuration by an agreed name and to properties the
  application supplies, and document both in the library's README.

## Exchange as a Maven repository

- **The organization-scoped URL only serves that organization's assets.**
  `https://maven.<region>.anypoint.mulesoft.com/api/v3/organizations/<org>/maven`
  does not serve MuleSoft's own Exchange connectors (Google Pub/Sub and others
  not on the EE Nexus); `https://maven.<region>.anypoint.mulesoft.com/api/v3/maven`
  does, with the same credentials. A dependency that resolves in CI but not
  locally usually means one `settings.xml` declares the second URL and the
  other does not.
- **A parent POM is a custom asset.** Plain `mvn deploy` does not publish it;
  `exchange-mule-maven-plugin` does, declared with `<inherited>false</inherited>`
  so children do not inherit it. Its `exchange-pre-deploy` goal is bound to
  `validate` and calls Exchange, so every build of the parent — even
  `mvn verify` — needs credentials and fails on a refused version.
- **Exchange never takes a version twice, even a deleted one.** `There is a
  deleted asset with the same version number` means bump the version.
- **Publishing needs Exchange Contributor.** A Connected App with only read
  access resolves dependencies and fails to publish with `User is not
  authorized to create an asset in this organization`.
- **Deploying needs its own scopes.** `Cannot get the environment, the business
  group is not valid` from `mule:deploy` is usually a Connected App missing
  View Environment, View Organization or the Runtime Manager scopes — not a
  wrong business group. Publication working says nothing about deployment.

## Writing a flow

```xml
<flow name="get-cart">
  <http:listener path="/carts/{id}" config-ref="HTTP_Listener_config"/>
  <set-variable variableName="cartId" value="#[attributes.uriParams.id]"/>
  <db:select config-ref="Database_Config">
    <db:sql>SELECT * FROM carts WHERE id = :id</db:sql>
    <db:input-parameters>#[{ id: vars.cartId }]</db:input-parameters>
  </db:select>
  <ee:transform>
    <ee:message><ee:set-payload resource="carts/to-api.dwl"/></ee:message>
  </ee:transform>
  <error-handler>
    <on-error-continue type="DB:CONNECTIVITY">
      <raise-error type="CART:BACKEND_UNAVAILABLE" description="Cart store unreachable"/>
    </on-error-continue>
  </error-handler>
</flow>
```

Keep transformations in `.dwl` files under `src/main/resources` rather than
inline in the XML once they outgrow a line or two — they are then testable and
reviewable on their own.

## Writing an MUnit test

```xml
<munit:test name="get-cart-404s-when-missing">
  <munit:behavior>
    <munit-tools:mock-when processor="db:select">
      <munit-tools:then-return>
        <munit-tools:payload value="#[[]]"/>
      </munit-tools:then-return>
    </munit-tools:mock-when>
  </munit:behavior>
  <munit:execution>
    <flow-ref name="get-cart"/>
  </munit:execution>
  <munit:validation>
    <munit-tools:assert-that expression="#[attributes.statusCode]"
                             is="#[MunitTools::equalTo(404)]"
                             message="Missing cart should 404"/>
  </munit:validation>
</munit:test>
```

Behavior sets preconditions, execution runs only the code under test,
validation asserts. Keeping to that split makes a failure legible: a validation
failure is a wrong result, an execution failure is a crash.

## Secrets

Configuration values are referenced as `${property}` and resolved from property
files, system properties or an encrypted secure-properties file. Never write a
credential into configuration XML, a property file or an MUnit fixture. Encrypted
values appear as `![ciphertext]`; the decryption key is supplied at runtime, not
committed. List sensitive property names in `secureProperties` in
`mule-artifact.json` so the runtime masks them in logs.

## Attribution

`references/` is derived from MuleSoft's official documentation. See
`ATTRIBUTION.md` for sources, licences, pinned versions and how to re-sync.
