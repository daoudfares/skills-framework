# Transactions, retries and reliability

> Derived from mulesoft/docs-mule-runtime (BSD 3-Clause).

## Transaction Management

Transactions are operations in a Mule app for which the result cannot remain indeterminate. When a series of steps in a flow must succeed or fail as one unit, Mule uses a transaction to demarcate that unit.

For example, you might use a transaction to encapsulate several steps in a flow that result in committing information to a database. In this type of scenario, the commit (or transaction) is either entirely complete and succeeds, or is incomplete and fails. Even if partially complete, the commit fails. When a transaction fails, Mule rolls back the operations within the transaction so that no part results in partial completion.

Implement a Reliability Pattern to design your application so it is capable of reliable messaging, even if the application receives messages from a non-transactional connector.

You can also configure Bitronix to manage transactions in your Mule application.

### Transaction Types

Mule supports Single Resource (Local, the default) and Extended Architecture (`XA`) transaction types (`transactionType`). The only components that can define the transaction type are event sources (for example, `jms:listener` and `vm:listener`) and the Try scope.

The following table describes the characteristics of each transaction type and the requisites for an operation to join the transaction:

| Transaction Type | Characteristics | Requisites to Join the Transaction |
|---|---|---|
| Single Resource (Local) |  · Performs better than XA transactions. · Does not support nested transactions. |  · The operation must support transactions. · All operations inside the transaction must belong to the same Connector. (For example `jms:listener`, `jms:consume` and `jms:publish`). · All operations must use the same Global Configuration (`config-ref`). |
| Extended Architecture (XA) |  · Involves using a two-phase commit protocol (2PC). · Slower but more reliable than Single Resource transactions. · Supports nested transactions. |  · The operation must support transactions. |

### Transactional Actions

A Transactional Action (`transactionalAction`) defines the type of action that operations take regarding transactions. The following table describes all available transactional actions:

| Action | Behavior | Available in |
|---|---|---|
| `ALWAYS_BEGIN` | Always start a new transaction when receiving a message. If a Single Resource transaction exists, an error occurs. If an XA transaction exists, a nested transaction is created. |  · Listeners that support transactions · Try scope |
| `ALWAYS_JOIN` | Always expect a transaction to be in progress when a message is received. If there is no transaction, an error occurs. |  · Operations that support transactions |
| `BEGIN_OR_JOIN` | If a transaction is already in progress when a message is received, join the transaction if possible. Otherwise, start a new transaction. |  · Try scope |
| `JOIN_IF_POSSIBLE` | Join the current transaction if one is available. Otherwise, no transaction is created. |  · Operations that support transactions |
| `INDIFFERENT` | Do not treat actions as a transaction. |  · Try scope |
| `NONE` | Do not initiate a transaction. |  · Listeners that support transactions |
| `NOT_SUPPORTED` | Execute outside any existent transaction. |  · Operations that support transactions |

### Configuring a Transaction in the Event Source

You can start a transaction from a Mule event source. In this case, the entire flow becomes a transaction. This is useful when working with messaging connectors to prevent the consumption of the message if a problem occurs when processing it, allowing you to retry later (because of the rollback).

To initiate a transaction from a Mule event source, configure its Transaction type and Transactional action:

- In Anypoint Studio
Open the Listener's **Advanced** tab, and set the **Transaction type** and the **Transactional action** values:

- In the Configuration XML
Add the `transactionalAction` element and the `transactionType` element (if necessary), and set their values.
The XML example below illustrates a `vm:listener` event source configured to initiate a Single Resource (Local) transaction:
```xml
[source,xml]
```

<?xml version="1.0" encoding="UTF-8"?>
<mule xmlns:http="http://www.mulesoft.org/schema/mule/http" xmlns:vm="http://www.mulesoft.org/schema/mule/vm"
	xmlns="http://www.mulesoft.org/schema/mule/core"
	xmlns:doc="http://www.mulesoft.org/schema/mule/documentation" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.mulesoft.org/schema/mule/core http://www.mulesoft.org/schema/mule/core/current/mule.xsd
http://www.mulesoft.org/schema/mule/vm http://www.mulesoft.org/schema/mule/vm/current/mule-vm.xsd
http://www.mulesoft.org/schema/mule/http http://www.mulesoft.org/schema/mule/http/current/mule-http.xsd">

	<vm:config name="VM_Config1" >
		<vm:queues >
			<vm:queue queueName="input" />
			<vm:queue queueName="output" />
		</vm:queues>
	</vm:config>

	<flow name="source-transactionsFlow">
		<vm:listener config-ref="VM_Config1" queueName="input" transactionalAction="ALWAYS_BEGIN"/>
		<http:request method="GET" url="www.google.com"/>
		<vm:publish config-ref="VM_Config1" queueName="output"/>
	</flow>
</mule>
```text
```

### Configuring a Transaction in a Try Scope

A Mule flow can also begin with a non-transactional connector (such as HTTP) that requires a transaction within the flow. For example, a Mule flow might accept information from an external Web service, then transform the data before charging a credit card and saving invoice information to a database. In such a situation, you use the Try scope to set up a transaction by wrapping the credit card charge and database commit operations within a transaction to ensure either complete success or complete failure and rollback.

You can configure a transaction in a Try scope component by setting a Transaction type and Transactional action:

- In Anypoint Studio
Open the Try scope's **General** tab, and set the **Transaction type** and the **Transactional action** values:

- In the Configuration XML
Add the `transactionalAction` element and the `transactionType` element (if necessary), and set their values.
In the following XML example the Try scope demarcates a transaction that includes a Database operation (`db:insert`) and a VM operation (`vm:publish`). Either both will be applied if the entire process succeeds, or none will be applied if an error occurs within the Try scope:
```xml
[source,xml]
```

<?xml version="1.0" encoding="UTF-8"?>
<mule xmlns:vm="http://www.mulesoft.org/schema/mule/vm" xmlns:db="http://www.mulesoft.org/schema/mule/db"
	xmlns="http://www.mulesoft.org/schema/mule/core"
	xmlns:doc="http://www.mulesoft.org/schema/mule/documentation"
	xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.mulesoft.org/schema/mule/core http://www.mulesoft.org/schema/mule/core/current/mule.xsd
http://www.mulesoft.org/schema/mule/db http://www.mulesoft.org/schema/mule/db/current/mule-db.xsd
http://www.mulesoft.org/schema/mule/vm http://www.mulesoft.org/schema/mule/vm/current/mule-vm.xsd">
	<db:config name="Database_Config">
		<db:derby-connection database="myDb" create="true" />
	</db:config>
	<vm:config name="VM_Config">
		<vm:queues>
			<vm:queue queueName="myQueue" />
		</vm:queues>
	</vm:config>
	<flow name="transactionsFlow">
		<try transactionalAction="ALWAYS_BEGIN" transactionType="XA">
		    <db:insert doc:name="Insert" transactionalAction="ALWAYS_JOIN">
	                  <db:sql>
				  INSERT INTO main_flow_audit (errorType, description) VALUES (:errorType, :description)
	                  </db:sql>
	                  <db:input-parameters><![CDATA[
	                     #[{
	                         'errorType' : 'AUTHENTICATION',
	                         'description' : 'invalid authentication credentials',
	                      }]
	            ]]></db:input-parameters>
	             </db:insert>
		     <vm:publish config-ref="VM_Config" queueName="myQueue" transactionalAction="ALWAYS_JOIN"/>
		</try>
	</flow>
</mule>
```text
```

### How Transactions Affect Scopes and Routers

When running in a transactional scope, the entire process must run in the same thread. This can change the way a scope executes, or how a transaction is handled. Below is detailed the behavior of the scopes and routers you must consider when running in a transactional scope:

#### Scopes

- Async: When running within a transaction, the Async scope will still run in another thread (remaining asynchronous). However, this means that the entire execution of the processors within this scope is out of the transactional scope. Therefore, any error produced inside an Async scope does not result in a rollback.
- Until Successful: When running within a transaction, the Until Successful scope blocks the thread. This means that the thread used by this execution cannot be used to process any other request while the Until Successful scope is performing the delay between retries.
- Parallel Foreach: When running within a transaction, the Parallel Foreach scope does not execute in parallel. This means it executes as the Foreach scope: the second element of the collection is processed after the first one has finished. This does not affect the way this scope handles errors.
- Batch Processing: Since Batch Processing is designed to work on parallel as the Async scope, and every record is treated transactionally (with internal Batch transactions), the batch execution is not part of the transaction.

#### Routers

- Scatter Gather: When running within a transaction, Scatter Gather does not execute in parallel. This means that the second route is executed after the first one is processed, the third after the second one, etc. This does not affect the way this component handles errors.
- Flow Reference: If the flow (or subflow) being executed is running within a transaction, the execution of the flow (or subflow) referenced by the Flow Reference component continues with the same transaction. If the referenced flow has a Mule event source that begins a transaction (For example a `jms:listener` source with `transactionalAction="ALWAYS_BEGIN"`), the `transactionalAction` is ignored. The Flow Reference component executes the referenced flow components except for its event source.

Any other router or scope (for example, Foreach) continues with the transaction and its behavior is not modified.

### Error Handling

When an error occurs during a transaction, your application must either handle the error and continue or perform a rollback.

There are two types of error handlers, which behave differently when an error occurs during a transaction:

- On Error Propagate
  - If the `on-error-propagate` error handler is inside the `error-handler` scope corresponding to the component that began the transaction:
The transaction is rolled back before executing the processors of the `on-error-propagate` scope. This means that the processors inside the error handler do not run within the transaction.

  - If the `on-error-propagate` error handler is inside an element that did not start the transaction:
The transaction is not rolled back and the processors inside the `on-error-propagate` error handler run within the transaction. Remember that some scopes and routers behave differently when executing within a transaction.

- On Error Continue
The error is handled, the transaction remains active and is able to commit. The processors inside the `on-error-continue` run within the transaction.

#### Example: Error Occurs in Try Scope

Consider an example in which the event source (`jms:listener`) starts a transaction, which is continued by the Try scope (`transactionalAction` is set to default, `INDIFFERENT`).

When the error occurs, it is handled by the `error-handler` of the Try scope first. The error is handled by an `on-error-propagate` error handler, but the transaction is not rolled back because it was not the Try scope that started the transaction. Only the flow error handler can roll back the transaction, because the transaction was initiated at flow level (from its event source).

The `jms:publish` operation inside the `on-error-propagate` error handler joins the transaction. The error is then propagated to the flow `error-handler`, which handles the error with an `on-error-continue` error handler. The `jms:consume` operation inside the `on-error-continue` error handler runs within the transaction. Finally, the transaction is committed.

```xml
<flow name="someFlowWithTx">
	<jms:listener config-ref="JMS_Config" destination="test.in" transactionalAction="ALWAYS_BEGIN"/>
	<!-- Processors -->
	<try>
		<raise-error type="APP:SOME"/>
		<error-handler>
			<on-error-propagate>
				<jms:publish config-ref="JMS_Config" destination="test.out" transactionalAction="ALWAYS_JOIN"/>
			</on-error-propagate>
		</error-handler>
	</try>
	<error-handler>
		<on-error-continue>
			<jms:consume config-ref="JMS_Config" destination="test.in2" transactionalAction="ALWAYS_JOIN"/>
		</on-error-continue>
	</error-handler>
</flow>
```

If the `on-error-continue` error handler is replaced with an `on-error-propagate` error handler in the previous example, then the transaction is rolled back before the execution of the processors. In this scenario, the configuration is not correct because the `jms:consume` operation cannot join any transaction.

#### Example: Error Occurs in a Referenced Flow

The following example behaves the same as the previous one, but instead of having a Try scope it uses a Flow Reference and the error occurs in the referenced flow:

```xml
<flow name="someFlowWithTx">
	<jms:listener config-ref="JMS_Config" destination="test.in" transactionalAction="ALWAYS_BEGIN"/>
	<!-- Processors -->
	<flow-ref name="someFlowContinuesTx"/>
	<error-handler>
		<on-error-continue>
			<jms:consume config-ref="JMS_Config" destination="test.in2" transactionalAction="ALWAYS_JOIN"/>
		</on-error-continue>
	</error-handler>
</flow>

<flow name="someFlowContinuesTx">
	<raise-error type="APP:SOME"/>
	<error-handler>
		<on-error-propagate>
			<jms:publish config-ref="JMS_Config" destination="test.out" transactionalAction="ALWAYS_JOIN"/>
		</on-error-propagate>
	</error-handler>
</flow>
```

Because the `someFlowContinuesTx` flow did not initiate the transaction, its error handler does not roll back the transaction.

#### Example: Comparing Error Handlers

This example shows the differences between the `on-error-continue` error handler and the `on-error-propagate` error handler:

```xml
<flow name="flow1">
	<jms:listener config-ref="JMS_Config" destination="test.in" transactionalAction="ALWAYS_BEGIN"/>
	<raise-error type="APP:SOME"/>
	<error-handler>
		<on-error-continue>
			<try transactionalAction="ALWAYS_BEGIN">
				<logger message="hello"/>
			</try>
		</on-error-continue>
	</error-handler>
</flow>

<flow name="flow2">
	<jms:listener config-ref="JMS_Config" destination="test.in" transactionalAction="ALWAYS_BEGIN"/>
	<raise-error type="APP:SOME"/>
	<error-handler>
		<on-error-propagate>
			<try transactionalAction="ALWAYS_BEGIN">
				<logger message="hello"/>
			</try>
		</on-error-propagate>
	</error-handler>
</flow>
```

In `flow1`, the `on-error-continue` error handler keeps the transaction active, but the Try scope inside it tries to initiate a new transaction. The configuration is not valid and results in an error.

In `flow2`, the `on-error-propagate` error handler rolls back the transaction, the processors inside the `on-error-propagate` error handler are executed, and a new transaction is created. This configuration is correct.

## Single Resource Transactions

Single Resource Transactions (also known as a simple transaction or local transaction) only use a single resource to send or receive messages: JMS broker, VM queues, or JDBC connections.

The example below illustrates a flow which includes a single resource transaction performed using the source and publish operations of the JMS connector.

```xml
<flow name="asdFlow" doc:id="2a67b1ee-0394-44a8-b6d9-9ce4f94f1ae2" >
	<jms:listener config-ref="JMS_Config" destination="test.in" transactionalAction="ALWAYS_BEGIN"/>
	<!-- Other operations -->
	<jms:publish config-ref="JMS_Config" destination="test.out" transactionalAction="ALWAYS_JOIN"/>
</flow>
```

Both the `jms:listener` source and the `jms:publish` operation must use the same connection configuration since this mechanism is intended to manage one resource.

The example shown above defines a JMS event source that receives messages from a `test.in` queue and another JMS operation that sends messages to a `test.out` queue. The `transactionalAction` attribute dictates how Mule initiates a transaction. Within this flow, Mule starts a new transaction for every message it receives (`jms:listener` source), and always joins the transaction in progress for every message it sends (`jms:publish` operation).

Mule only commits messages that successfully pass through the complete flow. If at any point in the flow a message throws an error which is propagated (i.e. it is not handled by an `on-error-continue`), Mule rolls back the transaction. Refer to On Error Scope for details on how to handle errors.

### Nested Transactions

Nested transactions are not available for Single Resource transactions. Refer to XA Transactions for more details.

## XA Transactions

Extended Architecture Transactions (or XA Transactions) can be used to group a series of operations from multiple transactional resources, such as VM, JMS or Database, into a single reliable global transaction.

The XA (eXtended Architecture) standard is an X/Open group standard which specifies the interface between a global transaction manager and local transactional resource managers. The XA protocol defines a 2-phase commit protocol which can be used to reliably coordinate and sequence a series of atomic operations across multiple servers of different types. Each local XA resource manager supports the A.C.I.D properties (Atomicity, Consistency, Isolation, and Durability) which help guarantee completion of a sequence of operations in the resource managed by the XA resource manager. Examples of transactional systems which often include local XA resource managers include databases, application servers, messaging queues, and transactional caches.

The global transaction manager is responsible for coordinating the transactional semantics of the global transaction between all the local XA transaction managers participating in the global transaction. To do this, each prepare and commit phase in the 2-phase commit is coordinated globally (often over the network) with each local XA resource manager.

The advantage of XA global transactions is that one global transaction manager can communicate and coordinate with multiple different transactional resources in a common and standard way. If any of the local resource managers report an error in the global transaction, the global transaction manager coordinates the rollback of any already prepared operations in each of the other local resource managers.
For example, a global transaction might include several operations to one or more databases, as well as messages sent to a JMS server on one or more topics. If anything goes wrong in the transaction, the global transaction manager guarantees that every resource is reset to the state before the global transaction was started. This keeps developers from having to include complex rollback or recovery logic outside the application.

The disadvantage of XA global transactions is that they can add tremendous latency to your transactions, especially if the resources are distributed over slow or unreliable network connections, and it can be difficult to recover if there are physical failures of systems in the middle of a globally distributed transaction.

### Performance Considerations

A global XA transaction is a reliable way of coordinating multiple XA resources, but it often increases latency and also requires additional resources such as an external transaction manager. A global transaction is only as reliable as the global transaction manager itself. For greater reliability, you need to use a transaction manager that also persists the state of each XA resource as the global transaction progresses through the prepare and commit phases, in case the transaction manager fails or loses network connectivity to any of the local XA resource managers during the global transaction.

### Configuring your Resource to use XA Transactions

To configure the event sources that support XA transactions, refer to the Connectors documentation:

- JMS Connector
- IBM MQ Connector
- VM Connector
- Database Connector

### Configuring a Try Scope to use XA Transactions

To configure a Try Scope to use XA Transactions, follow these steps:

1. Add the Try Scope from the Mule Palette.
2. Go to the **General** tab in the Try configuration panel.
3. Configure the Try Scope `Transactional Action` to `ALWAYS_BEGIN`, and the `Transaction Type` to `XA`.

See also Try Scope Concept for more information on how Try Scope handles transactions.

### Using XA Transactions with Different Resources

Regardless of how the Transaction is started (either from a Transactional event source or from a Try Scope), any Connector Operation that supports Transactions may join the Transaction by setting its Transactional Action to `ALWAYS_JOIN` or `JOIN_IF_POSSIBLE`.
XA Transactions are prepared to work with different resources, this means that operations from different resources can join the transaction. For example:

```xml
<flow name="exampleFlow" >
	<try transactionalAction="ALWAYS_BEGIN" transactionType="XA">
		<set-payload value="Hello World"/>
		<vm:publish queueName="someVmQueue" config-ref="VM_Config"/>
		<jms:consume config-ref="JMS_Config" destination="someQueue"/>
		<db:insert config-ref="Database_Config">
			<db:sql>${insertQuery}</db:sql>
		</db:insert>
	</try>
	<error-handler>
		<on-error-propagate enableNotifications="true" logException="true"/>
	</error-handler>
</flow>
```

If the `db:insert` operation fails, the transaction is rolled back before the error handler (`on-error-propagate`) is executed. Therefore, the message sent through the `vm:publish` is not confirmed to be sent, and
the message in the `jms:consume` is not actually consumed, so it is available next time to be consumed again.

In the following example, the error handler is changed to an `on-error-continue`:

```xml
<flow name="exampleFlow" >
	<try transactionalAction="ALWAYS_BEGIN" transactionType="XA">
		<set-payload value="Hello World"/>
		<vm:publish queueName="someVmQueue" config-ref="VM_Config"/>
		<jms:consume config-ref="JMS_Config" destination="someQueue"/>
		<db:insert config-ref="Database_Config">
			<db:sql>${insertQuery}</db:sql>
		</db:insert>
	</try>
	<error-handler>
		<on-error-continue enableNotifications="true" logException="true">
			<jms:publish config-ref="ANOTHER_JMS_Config" destination="someOtherQueue" transactionalAction="ALWAYS_JOIN"/>
		</on-error-continue>
	</error-handler>
</flow>
```

If the `db:insert` operation fails, the transaction is not rolled back. Instead, the Transaction is committed after the `jms:publish` (which runs within the XA Transaction) executes. Therefore, the message sent using `vm:publish` is published, the message from `jms:consume` is consumed, and the message sent using `jms:publish` is also published.

Consider that the `jms:publish` inside the `on-error-continue` has another configuration for the connector. This is not required but is possible. With single source (local) Transactions, this is not a valid configuration, since all operations that join a Transaction must use the same Configuration to work as designed.

### Nested Transactions

XA Transactions support nested transactions. You can create a new transaction when already executing within a transaction by using the Try Scope. Therefore, operations that run within the new transaction are accountable to it. If the nested transaction is rolled back, it does not mean that its parent transaction is also rolled back. After the nested transaction finishes (either with a commit or a rollback), the parent transaction continues its execution.

For example:

```xml
<flow name="exampleFlow" >
	<try transactionalAction="ALWAYS_BEGIN" transactionType="XA">
		<vm:publish queueName="someVmQueue" config-ref="VM_Config"/>
		<try transactionalAction="ALWAYS_BEGIN" transactionType="XA"/>
			<jms:consume config-ref="JMS_Config" destination="someQueue"/>
			<db:insert config-ref="Database_Config">
				<db:sql>${insertQuery}</db:sql>
			</db:insert>
			<raise-error type="APP:SOME"/>
		</try>
		<error-handler>
			<on-error-continue/>
		</error-handler>
	</try>
</flow>
```

In the previous example, the first `try` Scope creates a transaction. Then, the second `try` Scope creates a second transaction. The `vm:publish` operation runs within the first transaction, the `jms:consume` and the `db:insert` run within the second transaction. When the error is raised, the second transaction is rolled back along with the `jms:consume` and the `db:insert` operations. However, the first `try` handles the error with an `on-error-continue`, so the first transaction commits along with the `vm:publish` operation.

Consider the following example:

```xml
<flow name="exampleFlow" >
	<try transactionalAction="ALWAYS_BEGIN" transactionType="XA">
		<vm:publish queueName="someVmQueue" config-ref="VM_Config"/>
		<try>
			<try transactionalAction="ALWAYS_BEGIN" transactionType="XA"/>
				<jms:consume config-ref="JMS_Config" destination="someQueue"/>
				<raise-error type="APP:SOME"/>
			</try>
			<error-handler>
				<on-error-continue/>
			</error-handler>
		</try>
		<db:insert config-ref="Database_Config">
			<db:sql>${insertQuery}</db:sql>
		</db:insert>
	</try>
</flow>
```

In this case, the second `try` scope does not create a transaction. It only provides error handling, so that the next operations can continue. The third `try` scope does create a transaction. Both `vm:publish` and `db:insert` run within the first transaction, and `jms:consume` operation runs within the second one. When the error is raised, the second operation is rolled back. The error is propagated and handled by the `on-error-continue` of the second `try` scope. After that, the first `try` scope continues with its execution (the `db:insert` operation), and the first transaction is committed.

## Reconnection Strategies

When an operation in a Mule application fails to connect to an external server, the default behavior is for the operation to fail immediately and return a connectivity error.

For example, if an operation in Anypoint Connector for FTP (FTP Connector) fails to connect to an FTP server, the operation throws an `FTP:CONNECTIVITY` error. The error name reflects the namespace that is specific to the connector, such as `FTP:CONNECTIVITY`, or `DB:CONNECTIVITY` (for Anypoint Connector for Database (Database Connector).

You can modify this default behavior by configuring a reconnection strategy for the operation.

Operation executions don't trigger the reconnection strategy configured at the FTP Connector when failing with connectivity errors. In this example, the reconnection strategy applies only to the connection that `ftp:listener` needs to establish with the FTP server to query for new or updated files.

### Configure an Operation Reconnection Strategy

You can configure a reconnection strategy for an operation either by modifying the operation properties or by modifying the configuration of the global element for the operation. For example, you can configure a reconnection strategy in an FTP Connector configuration:

The following are the available reconnection strategies and their behaviors:

- **None**
Is the default behavior, which immediately returns a connectivity error if the attempt to connect is unsuccessful
- **Standard** (`reconnect`)
Sets the number of reconnection attempts and the interval at which to execute them before returning a connectivity error
- **Forever** (`reconnect-forever`)
Attempts to reconnect continually at a given interval

### Example XML Reconnection Strategy Configurations

The following examples show different types of reconnection strategies and their configurations:

- Standard reconnection strategy example
The following example illustrates a Standard reconnection strategy in an FTP connector configuration, setting the count of reconnection attempts before failing to `5` and setting `failsDeployment` to `true`, which causes the application deployment to fail if the connection test fails. Because a frequency is not specified, the retry interval is the default of every 2000 ms:
```xml
<ftp:config name="FTP_Config" doc:name="FTP Config" >
  <ftp:connection host="ftp.someftphost.com" port="21" username="myusername" password="mypassword" >
    <reconnection failsDeployment="true" >
      <reconnect count="5"/>
    </reconnection>
  </ftp:connection>
</ftp:config>
<flow name="reconnectionsFlow" >
  <ftp:listener doc:name="On New or Updated File" config-ref="FTP_Config">
    <scheduling-strategy >
      <fixed-frequency />
    </scheduling-strategy>
  </ftp:listener>
</flow>
```

- Forever reconnection strategy example
The following example sets a Forever reconnection strategy in an FTP connector configuration by which the connector attempts to reconnect every 4000 ms for as long as the application runs:
```xml
<ftp:connection host="ftp.someftphost.com" port="21" username="myusername" password="mypassword" >
  <reconnection>
    <reconnect-forever frequency="4000"/>
  </reconnection>
</ftp:connection>
```

### Reconnection Strategy Reference

Following are the different configuration attributes for each reconnection strategy you can configure by editing your Mule application's XML configuration file:

- Attributes of `<reconnection>`
| Name | Type | Required | Default | Description |
|---|---|---|---|---|
| `failsDeployment` | boolean | no | false | If `true`, causes the deployment to fail when the test connection fails |

- Attributes of `<reconnect>`
| Name | Type | Required | Default | Description |
|---|---|---|---|---|
| `blocking` | boolean | no | true | If `false`, the reconnection strategy runs in a separate, nonblocking thread |
| `frequency` | long | no | 2000 | How often (in ms) to reconnect |
| `count` | integer | no | 2 | How many reconnection attempts to make |

- Attributes of `<reconnect-forever>`
| Name | Type | Required | Default | Description |
|---|---|---|---|---|
| `blocking` | boolean | no | true | If `false`, the reconnection strategy runs in a separate, nonblocking thread. |
| `frequency` | long | no | 2000 | Specifies how often (in ms) to reconnect. |

## Configure a Redelivery Policy

A redelivery policy is a filter that helps you conserve resources by limiting the number of times the Mule runtime engine (Mule) executes messages that generate errors. You can add a redelivery policy to any source in a flow.

When you add a redelivery policy to a flow's source, Mule evaluates the received data before it executes the flow's components. If a message delivery fails a specified number of times, the redelivery policy prevents the flow from processing the received data and raises a REDELIVERY_EXHAUSTED error.

### Redelivery Policy Configuration Parameters

| Field | Type | Default Value | Description |
|---|---|---|---|
| **Max Redelivery Count** | Number | 5 | Maximum number of times that a message can be redelivered to the flow and processed unsuccessfully before raising a MULE:REDELIVERY_EXHAUSTED error. |
| **Use Secure Hash** | Boolean | True | Indicates whether to use a secure hash algorithm to identify a redelivered message. |
| **Message Digest Algorithm** | String | SHA-256 | Secure hashing algorithm to use for the message. If the payload of the message is a Java object, Mule ignores the **Message Digest Algorithm** value and returns the value that the payload's `hashCode()` returned. |
| **ID Expression** | Expression | - | Defines one or more expressions that determine when a message has been redelivered. This property can be set only if the value of **Use Secure Hash** is False. |
| **Object Store** | String | Object Store created by Mule's default `ObjectStoreManager`. Nonpersistent, with an `entryTtl` of 300 seconds and an `expirationInterval` of 6 seconds. | Object Store in which the redelivery counter for each message is stored. You can configure the Object Store as a reference or an inner element. For information, see the Object Store connector documentation. |

### How the Redelivery Policy Works

Each time the source receives a new message, Mule identifies the message by generating its key.

- If the processing flow causes an exception, Mule increments the counter associated with the message key. When the counter reaches a value greater than the configured **maxRedeliveryCount** value, Mule throws a MULE:REDELIVERY_EXHAUSTED error.
- If the processing flow does not cause an exception, its counter is reset.

### Errors

- MULE:REDELIVERY_EXHAUSTED
Thrown when the number of executions that raise an error is greater than the configured **maxRedeliveryCount** value.

### Example

In this example, Mule logs an error with a `Redelivery exhausted in http listener` message when the **maxRedeliveryCount** of 2 is exceeded:

```xml
<flow name="logOnRedeliveryExhausted">
    <http:listener path="test" config-ref="listenerConfig">
        <redelivery-policy maxRedeliveryCount="2" useSecureHash="true"/>
    </http:listener>
    <flow-ref name="processData"/>
    <error-handler>
        <on-error-continue type="MULE:REDELIVERY_EXHAUSTED">
            <logger message="Redelivery exhausted in http listener" level="ERROR"/>
        </on-error-continue>
    </error-handler>
</flow>
```

## Reliability Patterns

A reliability pattern is a design that results in reliable messaging for an application, even if the application receives messages from a nontransactional connector. A reliability pattern couples a reliable acquisition flow with an application logic flow, as shown in the following diagram:

The reliable acquisition flow (the left side of the diagram) delivers a message reliably from a Mule event source that does not implement transactions to an outbound operation of a connector that implements transactions. The operation can be of any type of the transactional endpoints, such as VM or JMS. If the reliable acquisition flow cannot deliver the message, it ensures that the message isn't lost.

- For socket-based connections like HTTP, this means returning an "unsuccessful request" response to the client so that the client can retry the request.
- For resource-based connections like File or FTP, it means not deleting the file, so that it can be reprocessed.

The application logic flow (the right side of the diagram) delivers the message from the event source that uses a transactional connector to the business logic for the application.

### Reliable Messaging

High-reliability applications must have zero tolerance for message loss. This means that both the underlying Mule and its individual connections need to be reliable.

If your application uses a transactional connection such as JMS, VM, or DB, reliable messaging is ensured by the built-in support for transactions in the connector. This means, for example, that you can configure a transaction on a JMS listener that makes sure messages are removed only from the JMS server when the transaction is committed. Doing this ensures that if an error occurs while processing the message, it is still available for reprocessing. In other words, the transactional support in these connectors ensures that messages are delivered reliably from a source to an operation, or between processors within a flow.

If you want to move messages between different connectors that support transactions, use XA transactions to ensure that both connectors' transactions are committed as one atomic unit.

See Transaction Management for more information about XA and other types of transactions.

If you have a web application that uses a nontransactional connector, such as HTTP, follow a reliability pattern to ensure reliable messaging for your application.

### Comparing Endpoints in Reliability Patterns

You can couple the reliable acquisition flow with any type of transactional endpoint. You don't have to use a VM endpoint in a reliability pattern. The following diagram illustrates a reliability pattern where the reliable acquisition flow delivers a message to a JMS endpoint:

The following table lists the advantages and disadvantages of using VM, JMS, and JDBC endpoints in a reliable acquisition flow.

| Endpoint | Advantage | Disadvantage |
|---|---|---|
| File-based VM (standalone Mule) |  · Provided ready to use with Mule. There is no need for additional software. |  · Applies only to non-clustered environments. |
| JDBC |  · Depending on resources available, JDBC can hold a large amount of information. |  · Requires additional software (database server). · Can be complex to use since proper DBMS schemas are required. |
| JMS (enabled for persistence) |  · Applies to both clustered and non-clustered environments. |  · Requires additional software (message queue server). |

The comparison doesn't include in-memory persistence setups for VM and JMS because they can lose messages and are not considered reliable.

### Implementing a Reliability Pattern

Below is a code example that shows what a complete reliability pattern would look like, including the reliable acquisition flow and the application logic flow. In this example, the reliable acquisition flow part of the reliability pattern is HTTP-to-VM.

#### Example: HTTP to VM

```xml
[source,xml]
```

<http:listener-config name="HTTP_Listener_config" doc:name="HTTP Listener config" >
	<http:listener-connection host="0.0.0.0" port="8081" />
</http:listener-config>
<vm:config name="VM_Config" doc:name="VM Config" >
	<vm:queues >
		<vm:queue queueName="toTransactionalVM" queueType="PERSISTENT"/>
	</vm:queues>
</vm:config>
<flow name="reliable-data-acquisition">
<http:listener config-ref="HTTP_Listener_config" path="transactionalEndpoint"/>
<vm:publish config-ref="VM_Config" queueName="toTransactionalVM" sendCorrelationId="ALWAYS"/> <!--1-->
</flow>

<!-- This is the application logic flow in the reliability pattern.
	It is a wrapper around the sub-flow "business-logic-processing". -->
<flow name="main-flow">
	<vm:listener doc:name="Listener" config-ref="VM_Config" queueName="toTransactionalVM"
		transactionalAction="ALWAYS_BEGIN"/> <!--2-->
	<flow-ref name="business-logic-processing"/>
</flow>

<!-- In this sub-flow, the application starts processing the message. -->
<sub-flow name="business-logic-processing">
	<logger level="INFO" doc:name="Logger" />
	<!--
		This is where the actual business-logic is performed.
	-->
</sub-flow>
```text
```

1. The message is written to the VM queue. It is now available for processing by the main flow.
1. The message is read from the VM queue transactionally. This ensures that if an error occurs, the reading is rolled back and the message is reprocessed.

To test this XML example in Studio, add the VM connector dependency to your project's `pom.xml` file.

This example shows VM file persistency, which does not work on clusters.

### Implementing a Reliable Acquisition Flow

The example provided in implementing a reliability pattern showed a reliable acquisition flow for an HTTP listener to a VM publish operation. This scenario focuses on a reliable acquisition flow that has a nontransactional event source: FTP-to-VM (Or SFTP, FTPS).

In this case, a resource-based connection is used. When using resource-based connections, ensure to read the resource only once. This is done by setting `watermarkEnabled` to `true`.

Do not set the `auto-delete` parameter to `true` because doing so deletes the file as soon as the flow finishes, even if the processing is done by another flow. The same applies to `moveToDirectory`.

#### Example: FTP to VM

The following code implements a reliable acquisition flow from an FTP listener (On New or Updated File) to a VM queue by a publish operation:

```xml
<ftp:config name="FTP_Config">
	<ftp:connection host="localhost" username="max" password="mulesoft"/>
</ftp:config>

<flow name="reliable-data-acquisition">
	<ftp:listener config-ref="FTP_Config" watermarkEnabled="true" directory="someDirectory/in"> <!--1-->
		<scheduling-strategy >
			<fixed-frequency />
		</scheduling-strategy>
	</ftp:listener>
	<vm:publish config-ref="VM_Config" queueName="toTransactionalVM"/>
</flow>

<flow name="doc-examplesFlow">
	<vm:listener queueName="toTransactionalVM" config-ref="VM_Config" transactionalAction="ALWAYS_BEGIN"/>
	<set-variable value="#[attributes.filename]" variableName="filepath"/>
	<!-- File content is already present in payload -->
	<flow-ref name="business-logic-processing"/>
	<ftp:delete path="#[vars.filepath]"/> <!--2-->
</flow>
```

<1> To perform a transformation before publishing to VM, add a max redelivery count.
<2> If the file is not intended to be deleted, do not use the `ftp:delete` operation. The same applies if the intended operation is `ftp:move`.

A similar implementation is done for any other of the resourced-based connectors.

### General Considerations

When you implement a reliability pattern, consider the following points:

- When the connector (event source) allows it, always use a transaction.
- When you want to enlist multiple managed resources within the same transaction, use an XA transaction to bridge event sources.
- The reliability of JMS is tied to the MQ implementation and how it is configured. Most MQ implementations allow you to configure whether messages are stored only in memory, or persisted. You can achieve reliability only if you configure the MQ server to persistently store messages before sending them forward. Otherwise, you risk losing messages in case of an MQ server crash.
- Reliability has performance implications.
- If the outbound operation in the reliable acquisition flow is not transactional (for example, a flow from file-to-FTP), perform that operation inside a Try Scope. With this practice, you can confirm if the operation completes successfully or, in case it fails, log the error message.

## Store Application Data Using Object Stores

An object store is a facility for storing objects in or across Mule applications. Mule runtime engine (Mule) uses object stores to persist data for eventual retrieval. Internally, Mule uses object stores in various filters, routers, and other message processors that need to store states between messages.

Object stores are available in all deployment targets. If you deploy your application to CloudHub, you can also use Object Store V2.

### Use Cases

You can configure a custom object store to use in the following scenarios:

- When configuring an Idempotent Message Validator, to store the unique IDs in the specified object store.
- When configuring a Redelivery policy in a listener (HTTP, File, JMS, VM, Socket), to store the redelivery count in the specified object store.
- When configuring a Cache scope that uses a custom caching strategy, to store the cached data in the specified object store.
- When a custom component uses an object store to persist information.
- When storing or retrieving information from a Mule flow, by using Anypoint Connector for Object Store (Object Store Connector).

### Object Store Configuration

By default, each Mule application has an object store that is persistent and is always available to the app. You can also create custom object stores, which can be persistent or in-memory.

You can configure an object store as a global element, to be accessible for any component in your app, or configure a custom object store for a specific component that supports its usage.

#### Configure a Global Object Store

To configure a global object store that can be referenced by other components in your application, follow these steps in Anypoint Studio:

1. Open the **Global Elements** tab.
1. Click **Create**.
1. Select **Component configurations** > **Object Store**.
1. Complete the required configuration attributes and click **OK**. +

Alternatively, you can create a global object store by including the following code as a top-level element in your application XML:

```xml
<os:object-store name="myObjectStore"
   entryTtl="1"
   entryTtlUnit="HOURS"
   maxEntries="100"
   persistent="true"
   expirationInterval="30"
   expirationIntervalUnit="MINUTES" />
```

Configure each attribute with the desired value. +
See Object Store Reference for a definition of each XML attribute.

### Configure an Object Store for a Specific Component

You can configure an object store that is available only for a specific component. For example, to configure an object store for an Idempotent Message Validator, follow these steps in Anypoint Studio:

1. Open the **Idempotent Message Validator** properties.
1. In **Object Store**, select **Edit Inline**.
1. Complete the required configuration attributes and click **OK**. +

Alternatively, you can create the object store by including the object store configuration inside the component element in the XML configuration file:

```xml
<idempotent-message-validator doc:name="Idempotent Message Validator" >
  <os:private-object-store
    maxEntries="20"
    entryTtl="20"
    entryTtlUnit="MILLISECONDS"
    expirationInterval="20"
    expirationIntervalUnit="MILLISECONDS"
    config-ref="ObjectStore_Config" />
</idempotent-message-validator>
```

### Manage Data Using the Object Store Connector

The Object Store connector enables you to perform different operations to interact with the object stores in your Mule application. Example operations include Store, Retrieve and Remove.

See the Object Store Connector documentation for details about available operations and configuration examples.
