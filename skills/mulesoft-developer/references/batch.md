# Batch processing

> Derived from mulesoft/docs-mule-runtime (BSD 3-Clause).

## Batch Processing

Mule batch processing components are designed for reliable, asynchronous processing of larger-than-memory data sets. The components are the Batch Job, Batch Step, and Batch Aggregator. The Batch Job component automatically splits  source data and stores it into persistent queues, which makes it possible to process large data sets while providing reliability. In the event that the application is redeployed or Mule crashes, the job execution is able to resume at the point it stopped.

Mule batch processing components are exclusive to the Enterprise Edition (EE) version of Mule. The components are not available through the open source Mule kernel.

Common use cases for batch processing include:

- Synchronizing data sets between business applications, such as syncing contacts between NetSuite and Salesforce.
- Extracting, transforming and loading (ETL) information into a target system, such as uploading data from a flat file (CSV) to Hadoop.
- Handling large quantities of incoming data from an API to a legacy system.

See batch filters and batch aggregator and batch error handling faq for examples.

### Architecture

Mule batch processing components prepare records for processing in batches, run processors on those records, and issue a report on the results of the processing. Record preparation and reporting take place within the Batch Job component. Processing takes place within one or more Batch Step components and, optionally, a Batch Aggregator component within a Batch Step component.

The processors you place within batch processing components act on records. Each record is similar to a Mule event: Processors can access, modify, and route each record payload using the `payload` keyword, and they can work on Mule variables using `vars`. However, they _cannot_ access or modify Mule attributes (`attributes`) from the input to the Batch Job component.

The following example outlines the XML structure of a Mule flow that performs batch processing and returns a report with the results of that processing:

```xml
<flow name="mule-flow" >
  <!-- processor that triggers the flow -->
  <event source placeholder /><!--1-->
  <!-- message processors -->
  <processor placeholder /><!--2-->
  <processor placeholder />
  <!-- Batch Job component -->
  <batch:job name="Batch_Job"/><!--3-->
    <!-- record processing occurs within process-records -->
    <batch:process-records ><!--4-->
      <!-- Batch Step component -->
      <batch:step name="Batch_Step"/><!--5-->
        <!-- processors that act on records -->
        <processor placeholder />
        <processor placeholder />
        <!-- Batch Aggregator component -->
        <batch:aggregator /><!--6-->
          <!-- processor that acts arrays of records -->
          <processor placeholder />
        </batch:aggregator>
      </batch:step>
      <!-- another Batch Step component -->
      <batch:step name="Batch_Step1"/><!--7-->
        <!-- processor that acts on records -->
        <processor placeholder />
      </batch:step>
    </batch:process-records>
    <!-- processing of a batch job report takes place in on-complete -->
    <batch:on-complete><!--8-->
      <!-- processor for result of a batch job -->
      <processor placeholder />
    </batch:on-complete>
  </batch:job>
</flow>
</mule>
```

Note that the various `placeholder` entries in the example, such as `<processor placeholder />`, illustrate the location of real processors, such as connector operations, Mule core components, and so on, which process Mule messages, records, and the batch processing report. They are _not real processors_.

1. The Mule event source triggers the Mule flow. Common event sources are listeners, such as an HTTP listener from Anypoint Connector for HTTP (HTTP Connector), a Scheduler component, or a connector operation that polls for new files.
1. Processors located upstream of the Batch Job component typically retrieve and, if necessary, prepare a message for the Batch Job component to consume. For example, an HTTP request operation might retrieve the data to process, and a DataWeave script in a Transform Message component might transform the data into a valid format for the Batch Job component to receive.
1. When the Batch Job component receives a message from an upstream processor in the flow, the Load and Dispatch phase begins. In this phase, the component prepares the input for processing as records, which includes creating a batch job instance in which processing takes place.
1. The batch job instance executes when the batch job instance reaches `<process-records/>`. At this point, the Process phase begins. All record processing takes place during this phase.
1. Each Batch Step component contains one or more processors that act upon a record to transform, route, enrich, or modify data in the records. For example, you might configure a connector operation to pass processed records one-by-one to an external server.
1. A Batch Aggregator component is optional. You can add only one to a Batch Step component. The initial processor within a Batch Aggregator must be able to accept an array of records as input. Batch aggregation is useful for loading an array of processed records to an external server. It is also possible to use components, such as For Each, that iterate over the array so that other processors can process the records individually. The Batch Aggregator component requires a `streaming` or `size` setting to indicate how to process records.
1. Additional Batch Step components are optional. This example does not contain a Batch Aggregator component.
1. After records pass through all Batch Step components, Mule completes the batch job instance and reports the results in an object that indicates which records succeed and which failed during processing. You can retrieve or log the result with a Logger or other processor within `<batch:on-complete />`.
The Batch Job component consumes records in the On Complete phase, which occurs after all record processing in a batch job instance finishes, and does not propagate the processed records to external components, outside of the Batch Job component. However, like many Mule components, the Batch Job component provides a way to set a target variable (`target`) property that a downstream component, outside Batch Job use to gain access to the _pre-processed payload_ that the Batch Job component receives.

For more detail, see batch phases.

### Valid Input to the Batch Job Component

When triggered by an upstream event in the flow, the Batch Job component performs an implicit split operation on the Mule message input. The operation accepts any Java Iterables, Iterators, or Arrays, as well as JSON and XML payloads. The component cannot split any other data format.

If you are working with a data format that is not compatible with the splitting process, transform the payload to a supported format before it enters the Batch Job component.

### Mule Variable Propagation

Each record in a batch job instance inherits Mule event variables from the input to the Batch Job component. You can access and change the value of these variables in the Batch Step and Batch Aggregator components, which run during the Process phase, and you can create new variables within these components. For each record within this phase, the variables (and modifications to them) are propagated through each Batch Step and Aggregator component within a Batch Job component. For example, if record R1 sets the Mule variable `varName` to `"hello"`, record R2 sets `varName` to `"world"`, and record R3 does not set this variable, then in the next Batch Step component, R1 has the value `"hello"`, R2 the value `"world"`, and R3 returns `null` for that variable.

In a similar scenario, if `varName` is set in the flow _before_ the Batch Job component and record 3 (R3) does not change the value of `varName`, R3 inherits that value. To illustrate this point, assume a Mule flow that sends the Batch Job component a `payload` of the array `[1,2,3,4]` and a Mule variable `varName` with the value `"my variable before batch job"`. The following example uses the Choice router (`choice`) to set a new value for `varName` in the first and second records but not the third. Subsequent records also set a new `varName` value.

```xml
<flow name="batch-variables-ex" >
  <scheduler doc:name="Scheduler" >
    <scheduling-strategy >
      <fixed-frequency frequency="45" timeUnit="SECONDS"/>
    </scheduling-strategy>
  </scheduler>
  <!-- Set Payload -->
  <set-payload value="#[[1,2,3,4]]" doc:name="Set Payload" />
  <!-- Set Variable -->
  <set-variable value='"my variable before batch job"' doc:name="Set Variable"
                variableName="varName" />
  <!-- Log Variable -->
  <logger level="INFO" doc:name="Logger"
          message="#[vars.varName]"
          category="PRINT VARIABLE BEFORE BATCH" />
  <!-- Batch Job -->
  <batch:job jobName="batch-variables-exBatch_Job" >
    <batch:process-records >
      <!-- First Batch Step -->
      <batch:step name="Batch_Step" >
        <logger level="INFO" doc:name="Logger"
                message="#[payload]"
                category="PRINT RECORD NUMBER"/>
        <choice doc:name="Choice" >
          <!-- First record, R1 -->
          <when expression="#[payload == 1]">
            <set-variable value='"hello"' doc:name="Set Variable"
                          variableName="varName" />
            <logger level="INFO" doc:name="Logger"
                    message="#[vars.varName]"
                    category="R1: PRINT VARIABLE for PAYLOAD is 1"/>
          </when>
          <!-- Second record, R2 -->
          <when expression="#[payload == 2]">
            <set-variable value='"world"' doc:name="Set Variable"
                          variableName="varName" />
            <logger level="INFO" doc:name="Logger"
                    category="R2: PRINT VARIABLE for PAYLOAD is 2"
                    message="#[vars.varName]"/>
          </when>
          <!-- Third record, R3 -->
          <when expression="#[payload == 3]">
            <logger level="INFO" doc:name="Logger"
                    message="#[vars.varName]"
                    category="R3: PRINT VARIABLE for PAYLOAD is 3"/>
          </when>
          <!-- Other records -->
          <otherwise>
            <set-variable value='"some other value"' doc:name="Set Variable"
                          variableName="varName"/>
            <logger level="INFO" doc:name="Logger"
                    category="Rn: PRINT DEFAULT VARIABLE" message="#[vars.varName]"/>
          </otherwise>
        </choice>
      </batch:step>
      <!-- Second Batch Step -->
      <batch:step name="Batch_Step1" >
        <logger level="INFO" doc:name="Logger"
                message='#[("payload " ++ payload as String) : vars.varName]'
                category="PRINT VARIABLES IN SECOND STEP"/>
      </batch:step>
    </batch:process-records>
  </batch:job>
  <!-- Log Variables After Batch Job -->
  <logger level="INFO" doc:name="Logger"
          message="#[vars.varName]"
          category="PRINT VARIABLE VALUES AFTER BATCH JOB"/>
</flow>
```

The logs print the following messages for a batch job instance (edited for readability):

```text
...
INFO ...PRINT VARIABLE BEFORE BATCH: "my variable before batch job"
...
INFO ...PRINT VARIABLE VALUES AFTER BATCH JOB: "my variable before batch job"
INFO ...PRINT RECORD NUMBER: 1
INFO ...R1: PRINT VARIABLE for PAYLOAD is 1: "hello"
INFO ...PRINT RECORD NUMBER: 2
INFO ...R2: PRINT VARIABLE for PAYLOAD is 2: "world"
INFO ...PRINT RECORD NUMBER: 3
INFO ...R3: PRINT VARIABLE for PAYLOAD is 3: "my variable before batch job"
INFO ...PRINT RECORD NUMBER: 4
INFO ...Rn: PRINT DEFAULT VARIABLE: "some other value"
...
INFO ...PRINT VARIABLES IN SECOND STEP: {payload 1="hello"}
INFO ...PRINT VARIABLES IN SECOND STEP: {payload 2="world"}
INFO ...PRINT VARIABLES IN SECOND STEP: {payload 3="my variable before batch job"}
INFO ...PRINT VARIABLES IN SECOND STEP: {payload 4="some other value"}
...
```

Notice that the third record (R3) inherits the value of the `varName` set before the Batch Job component. Any records after R3 set the variable to `"some other value"`. Records logged in the second Batch Step inherit the values of the variables from the first Batch Step. The Logger _after_ the Batch Job component, which is processed asynchronously, _before_ the batch job instance finishes processing, also receives the value of `varName` _before_ the Batch Job executes, `"my variable before batch job"`.

Changes and additions to Mule variables during the Process phase do not propagate to the On Complete phase. Only variables inherited from the triggering event to the Batch Job component propagate to the On Complete phase, and standard variables that are part of the batch job report, such as `batchJobInstanceId`, are also present in this phase. It is possible to create a variable in the On Complete phase that persists through the phase but not after the On Complete ends.

For example, assume that the On Complete phase sets a new variable (`myOnCompleteVar`) and logs all variables (`vars`) found in this phase.

```xml
<batch:on-complete >
  <set-variable value="Hello On Complete Variable" doc:name="Set Variable"
                variableName="myOnCompleteVar"/>
  <logger level="INFO" doc:name="Logger"
          message="#[vars]"
          category="PRINT ON COMPLETE VARIABLES"/>
</batch:on-complete>
```

In the On Complete report, you find the final set variables for a batch job instance, for example:

```text
INFO ... PRINT ON COMPLETE VARIABLES: {
varName=TypedValue[value: '"my variable before batch job"', dataType: 'SimpleDataType{type=java.lang.String, mimeType='*/*; charset=UTF-8'}'],
batchJobInstanceId=TypedValue[value: '869ae510-5c84-11ed-bc38-147ddaaf4f97', dataType: 'SimpleDataType{type=java.lang.String, mimeType='*/*'}'],
myOnCompleteVar=TypedValue[value: 'Hello On Complete Variable', dataType: 'SimpleDataType{type=java.lang.String, mimeType='*/*; charset=UTF-8'}']}
```

Variables in the report object example follow:

- `varName` is an example of a variable created before reaching the Batch Job component. This variable retains the value it had when it entered the component. Any changes to the value during the Process phase are not retained in the On Complete phase.
- `batchJobInstanceId` is a standard variable that identifies a batch job instance.
- `myOnCompleteVar` is an example of a variable created within the On Complete phase. It appears in the report but does not persist after the On Complete phase ends.

Downstream from the Batch Job component, only `varName` persists. Like the records and their attributes, the variables of the records are completely consumed within the Batch Job component. The batch job instance executes asynchronously from the rest of the flow, so no variable created within the Process or On Complete phases persists outside of the Batch Job component.

### Error Handling

To prevent the failure of an entire batch job, the Batch Job component can handle any record-level failure that occurs. Further, you can set or remove variables on individual records so that during batch processing, Mule can route or otherwise act upon records in a batch job instance according to a variable. See Handling Errors During Batch Job for more information.

## Batch Job Phases

Each time a Batch Job component executes, it goes through these phases:

1. phase load dispatch: The Batch Job component splits valid input into records and prepares the records for processing. This phase takes place within the Batch Job component.
1. phase process: Mule components and connector operations within one or more Batch Step components in the Batch Job process records within a given batch job instance. Processing within a Batch Aggregator component also occurs in the Process phase.
1. phase on complete: The Batch Job component issues a report object with the result of processing the batch job instance.

For an example, see batch phase XML.

### Load and Dispatch Phase

When an upstream event in the flow triggers the Batch Job component, the Load and Dispatch phase begins. In this phase, these actions occur:

1. Mule creates a new batch job instance that persists through each phase of a batch job.
Within the scope of the Batch Job component, Mule exposes the currently processing batch job instance ID through the `batchJobInstanceId` variable. You can use `vars.batchJobInstanceId` to access the identifier of the current instance in any batch processing phase. The auto-generated identifier is a UUID, but you can change it to a different value. For details, see batch job instance id.
1. The Batch Job component automatically splits the received message payload into records and stores the records in the stepping queue.
The Batch Job component either successfully generates and queues a record for every item from the input, or the entire event fails with an error type, such as `MULE:EXPRESSION` message, and an error message, such as `"Expecting Array or Object but got String." evaluating expression: "payload".`
In Anypoint Runtime Manager, the queue name is prefixed with `BSQ`, for example:
1. The Batch Job component starts the execution of a batch job instance that processes the loaded records.

### Process Phase

The Process phase begins after the Load and Dispatch phase finishes loading records to the queue and starts execution of a batch job instance. In this phase, Batch Step components concurrently pull record blocks of the configured size from the queue to process them. (The default batch block size is 100.)

Within the Batch Step component, Mule processes multiple record blocks in parallel by using separate threads, while the records within each block process sequentially by default. Mule uses its auto-tuning capabilities to determine how many threads to use and the level of parallelism to apply (see Execution Engine).

During this phase, processors within the components can access and modify records using the `payload` and `vars` Mule variables. The Batch Job component consumes records after all record processing finishes. So any transmission of _processed_ records to an external server or service must take place _within_ the Batch Step or Batch Aggregator components. For Mule variable propagation rules, see Variable Propagation.

After processing records in a block, the Batch Step sends the records back to the stepping queue, where they become available for the next Batch Step component. The next Batch Step doesn't wait for the previous step to complete. It starts processing available records as soon as they return to the queue. Records are pulled from the queue in blocks, but the composition of these blocks can differ from the previous step because records from different parallel threads are mixed in the queue. At the end of this phase, all records are consumed and aren't available for further processing by downstream processors in the Mule flow.

Note that since changes to records that take place within a Batch Aggregator component _aren't propagated_ outside of Batch Aggregator component, changes aren't visible to subsequent Batch Step components in the flow.

As processing takes place, each record keeps track of all  Batch Step components that process it.

By default, a batch job instance doesn't wait for all its queued records to finish processing in one Batch Step component before making them available for processing by the next Batch Step component. Configuring a Batch Aggregator component changes this behavior:

- Behavior when the Batch Aggregator component sets a fixed size:
A processor within the Batch Aggregator must be able to receive the array of records as input.
1. Each Batch Step component within a Batch Job component receives one or more record blocks and starts processing them in parallel.
1. After processing a record, the Batch Step component sends the record to the Batch Aggregator component for further processing.
1. When set to process a fixed size (`size`), the Aggregator component arranges the records into one or more blocks containing the specified number of records. If fewer records are available than the configured size, the last block of records is smaller.
1. After processing records in a given array, the Batch Aggregator component sends all the records back to the stepping queue.

- Behavior when the Batch Aggregator component is configured to stream records:
When streaming, the Batch Aggregator component processes records as soon as it receives them instead of putting them into record blocks. No record is exposed to the _next_ Batch Step component in the flow until all the records in the Aggregator processes all records in the _current_ Batch Step.
A processor within the component must be able to accept an array of records as input.
1. Each Batch Step component receives one or more record blocks and starts processing them in parallel.
1. After the Batch Step processes a record, the Batch Step sends the record to Batch Aggregator for further processing.
1. The Batch Aggregator component continues processing records until there are no more records in the stepping queue that are waiting to be processed by the current Batch Step.
1. The Batch Aggregator component sends all the aggregated records to the stepping queue.

Mule retains a list of all records that succeed or fail to process through each Batch Step. If an event processor in a Batch Step fails to process a record, Mule continues processing the batch, skipping over the failed record in each subsequent Batch Step based on the `acceptPolicy`. The Batch Job component provides the `maxFailedRecords` property for setting the number records that can fail before the batch job stops. See Batch Job Properties.

### On Complete Phase

During this phase, you can configure Mule runtime to create a report or summary of the records it processed in a given batch job instance. This phase provides system administrators and developers insight into which records failed or succeeded, but it doesn't process or provide access to individual records, nor does it pass processed records to downstream processors in the flow.

At the end of this phase, the batch job instance completes and ceases to exist.

As a best practice, configure a mechanism for reporting on failed or successful records to facilitate further action where required. During the On Complete phase, you can perform either of these tasks:

- Reference the result object of the batch job instance from elsewhere in the Mule application to capture and use batch job metadata, such as the number of records that failed to process in a particular batch job instance.
- Log the result object for each batch job instance:

```xml
<batch:job name="Batch3">
  <batch:process-records>
    <batch:step name="Step1">
      <batch:record-variable-transformer/>
      <ee:transform/>
    </batch:step>
    <batch:step name="Step2">
      <logger/>
      <http:request/>
    </batch:step>
  </batch:process-records>
  <batch:on-complete>
    <logger level="INFO" doc:name="Logger"
            message='#[payload as Object]'/>
  </batch:on-complete>
</batch:job>
```

From the logger set to `payload as Object`, a report looks something like this:

```text
INFO  2022-07-06 11:39:02,921 [[MuleRuntime].uber.06:
[w-batch-take6].batch-management-work-manager @56978b97]
[processor: w-batch-take6Flow/processors/3/route/1/processors/0;
 event: e835b2c0-fd5a-11ec-84a5-147ddaaf4f97]
org.mule.runtime.core.internal.processor.LoggerMessageProcessor:
{onCompletePhaseException=null, loadingPhaseException=null, totalRecords=1000,
 onCompletePhaseError=null, elapsedTimeInMillis=117, failedOnCompletePhase=false,
 failedRecords=0, loadedRecords=1000, failedOnInputPhase=false,
 successfulRecords=1000, inputPhaseException=null,
 batchStepResults={firstError=com.mulesoft.mule.runtime.module.batch.privileged.ImmutableBatchStepResult@d9323a5},
 processedRecords=10, loadingPhaseError=null, failedOnLoadingPhase=false,
 batchJobInstanceId=e84b5da0-fd5a-11ec-84a5-147ddaaf4f97, inputPhaseError=null}
```

The fields in the batch job report object are accessible as keys when using DataWeave selectors, such as `payload.failedRecords` to return the number of failed records in the instance.

If you leave the On Complete phase empty, the batch job instance silently completes, and the logs provide processing information about the instance, for example:

```text
Finished execution for instance 'e84b5da0-fd5a-11ec-84a5-147ddaaf4f97'
of job 'w-batch-take6Batch_Job'.
Total Records processed: 1000. Successful records: 1000. Failed Records: 0
```

## Batch Component Reference

Mule batch components manage bulk processing of records with minimal adjustments to default component settings. They are highly configurable to meet specific processing and performance requirements.

A Batch Job component must contain at least one Batch Step component. Optionally, each Batch Step component can contain a single Batch Aggregator component. The Mule flow in the following figure shows batch components.

The Batch Job component splits the payload of the Mule message into records. Within the Batch Step and Batch Aggregator components, these records are available with the keyword `payload`, and Mule variables are also accessible through the `vars` keyword. However, Mule attributes are not accessible from within these components. Both components return `null` on `attributes`.

This reference assumes that you are familiar with the batch processing phases of a batch job instance.

### Batch Job Component (<batch:job />)

This component prepares its input for processing and outputs a report with results of that processing. Preparation takes place during the Load and Dispatch phase of a batch job instance, and the report is available in the On Complete phase.

In Studio, you can set these properties in the component's General and History tabs.

#### Batch Job Properties

The Batch Job component provides a number of configurable properties that determine how batch processing takes place. It also provides a way of storing the input payload in a target variable for use by subsequent components in the flow, which can be useful because the Batch Job component consumes the message payload.

Anypoint Studio provides the following fields in the **General** tab:

The following table describes each field and includes the XML attribute for the field.

| Field Name | XML | Description |
|---|---|---|
| Name | `name` | Configurable name for a Batch Job component. The default name appends `Batch_Job` to the name of the application. |
| Max Failed Records | `maxFailedRecords` | Maximum number of records that can fail within a batch job instance before the execution of that instance stops. The default is `0`. Use `-1` for no limit. This setting takes precedence over any accept policy (`acceptPolicy`) or expression (`acceptExpression`) filter on a Batch Step component within the Batch Job component. When a batch job instance exceeds the `maxFailedRecords` value, the Batch Job component stops processing of the batch job instance in which the failure occurs, assigns the instance the status `FAILED_PROCESS_RECORDS`, and reports the number of failed records in the instance. When a batch job instance reaches this threshold, the console prints a message such as this one (edited for readability): ---- INFO  ... DefaultBatchEngine: instance '6d85c380-f332-11ec-bb5f-147ddaaf4f97' of job 'Batch_Job_in_Mule_Flow' has reached the max allowed number of failed records. Record will be added to failed list and the instance will be removed from execution pool. ... INFO  ... DefaultBatchEngine: instance 6d85c380-f332-11ec-bb5f-147ddaaf4f97 of job Batch_Job_in_Mule_Flow has been stopped. Instance status is FAILED_PROCESS_RECORDS ---- Note that parallel processing within a batch job instance makes it possible for the number of errors to exceed the configured maximum because it is possible for multiple records fail at the same time. |
| Scheduling Strategy | `schedulingStrategy` | When a Batch Job component triggers repeatedly, more than one batch job instance can be ready to execute at the same time. The instances can run sequentially based on their creation timestamp (the default) or according to a round-robin algorithm that attempts to maximize the use of available resources. This setting is appropriate only for jobs that have no side effects or dependencies on other records because the order of processing is not guaranteed. · `ORDERED_SQUENTIAL` (default): With this setting, batch job instances execute one at a time in the order established by their creation timestamp. An instance created earlier executes before an instance created at a later time and date. · `ROUND_ROBIN`: With this setting, all batch job instances execute based on a round-robin algorithm that assigns available resources. Order of execution is not predetermined. Batch instances can execute in any order. This option is viable only if you are certain that no execution of an instance is capable of producing a side effect on an execution of another instance. Best practices: · To avoid potential updates to the same record in concurrently running batch job instances, do not use this strategy for data synchronization jobs. Using this strategy when synchronizing data makes it possible to return a result with an earlier, incorrect version of the data. · Use this strategy to parallelize execution of batch job instances if you are certain that no record depends on the processing of another record within the Batch Job component, such as a case in which your batch job retrieves only new records from a database. |
| Job Instance ID | `jobInstanceId` | Optional expression that provides a recognizable, unique name for the batch instance. To make the name unique, you must use a DataWeave expression, for example, `\#[jobInstanceId="#['Job From ' ++ now() as String {format: 'dd/MM/yy hh:mm:ss'}]` within this field. If an expression returns the same value more than once, Mule throws an error with a message such as, `Batch Job 'my-batch-job-example' already has an instance with id 'my-repeated-id'`. The Batch Job component uses this value to create a new identifier each time the Mule flow reaches the Batch Job component. If you do not provide an ID, Mule automatically creates a UUID that serves as the identifier for each batch job instance. |
| Batch Block Size | `blockSize` | Number of records to process per record block. The default is `100` records per block. If fewer records are available for processing than the configured size, Mule sends a block of a smaller size to the record processors. Such a case can occur, for example, if there are 1010 records and the block size is 100 because the modulo is 10, not 0. The block size setting provides a way to tune performance, which is affected by the size of records in each block and the `maxConcurrency` setting. |
| Max Concurrency | `maxConcurrency` | Property that sets the maximum level of parallelism to allow when processing record blocks within the component. The default is twice the number of cores available in the CPUs. The capacity of the system running the Mule instance also limits concurrency. Like the `blockSize` setting, this setting provides a way to tune performance. |
| Target | `target` | To use the payload received by a batch job instance in a component that is located _after_ the Batch Job component, you can provide a unique value for the `target` and use `payload` in the downstream component to gain access that payload. Without a target value, the input payload to the Batch Job component is not available in downstream components. For more information about target variables, see target variables. There is no default value. |

#### Batch Job History (<batch:history />)

A batch job history configuration enables you to address a `No space left on device` error by adjusting the amount of time that historical data for batch job instances persist in a temporary Mule directory. This error can occur if the frequency or number of records to process is too high for the available disk space or for a CloudHub worker of a given size to handle.

By default, the history of batch job instances persists for 7 days. A monitoring process automatically removes that history when the period expires.

The following table describes each field and includes the XML attribute for the field.

| Name | XML | Description |
|---|---|---|
| Max Age | `maxAge` | Maximum age of job instances before they expire, for example: `expiration maxAge="10"`. Default: `maxAge=7`. |
| Time Unit | `ageUnit` | The unit of time to apply to the `maxAge`. Valid values: `DAYS`, `HOURS`, `MILLISECONDS`, `MINUTES`, and `SECONDS`. Default: `ageUnit=DAYS`. |

Note that these fields are attributes to the `<batch:expiration/>` element, which is embedded within `<batch:history/>`:

```xml
<batch:job ...>
  <batch:history >
    <batch:expiration maxAge="10" ageUnit="MINUTES" />
  </batch:history>
  <batch:process-records>
    <batch:step />
  </batch:process-records>
<batch:job />
```

The XML example is edited to focus on settings in the batch history fields.

### Batch Step Component (<batch:step/>)

The Batch Step component runs during the Process phase of a batch job instance, not during the Load and Dispatch or On Complete phases.

A minimum of one Batch Step component is required within a Batch Job component. In addition to changing the name of a Batch Step component, you can configure _filters_ that determine which records the component accepts for processing within the component. Any processors that you add to the component act on records that the Batch Job component accepts.

The following table describes each field and includes the XML attribute for the field.

| Field Name | XML | Description |
|---|---|---|
| Name | `name` | Configurable name for a Batch Step component. The default is `Batch_Step` for the first Batch Step component within a Batch Job component. Subsequent steps append a unique number to the name, following the sequence, `Batch_Step1`, `Batch_Step2`, and so on. |
| Accept Expression | `acceptExpression` | Optional DataWeave expression for a filter that determines whether to process a record in the component. If _both_ the `acceptExpression` _and_ the `acceptPolicy` values for a record evaluate to `true`, then the component accepts the record for processing. If not, the component skips the record, and the record becomes available to any downstream Batch Step components. Examples: · `acceptExpression="#[payload.age > 21]"` for a payload with an `age` field · `acceptExpression="#[not isBlank(payload.name)]"` for a payload with a `name` field. |
| Accept Policy | `acceptPolicy` | Accepts a record for processing only if the policy evaluates to `true` for that record. You can base acceptance on the success or failure of a record to process successfully in _preceding_ (upstream) Batch Step components within the Batch Job component. You can configure the component to process only records that processed successfully, only records that failed to process successfully, or all records, regardless of whether they processed successfully. The default is `NO_FAILURES`. Note that the `acceptPolicy` evaluates before any `acceptExpression` on the component, and the `maxFailedRecords` setting on the Batch Job component takes precedence over `acceptPolicy` settings. · `NO_FAILURES`: Default setting. Accepts a record for processing if the record never failed to process successfully within a preceding Batch Step component or if there is no upstream Batch Step component. · `ONLY_FAILURES`: Accepts a record for processing if the record failed to process successfully within a preceding Batch Step component. · `ALL`: Accepts a record for processing regardless of processing successfully or failing within a preceding Batch Step component. |

### Batch Aggregator Component (<batch:aggregator />)

The Batch Aggregator component is an optional component that acts on an array of records. Aggregation takes place during the Process phase of a batch job instance.

There is no default configuration for the Batch Aggregator component. If you use this component, you must indicate whether to stream records (`streaming`) or pull records from the queue into separate arrays of a fixed size (`size`), but not both. The settings are mutually exclusive. Random access to streamed records is not possible.

The Batch Aggregator component accepts one or more processors for the message `payload`. However, it is common to use a scope within the aggregator, such as For Each scope, to iterate over each record so that the child processors within the scope can act on each record individually.

The Batch Aggregator component also provides a way preserve the MIME type of records (`preserveMimeTypes`), which is needed when accessing part of a record that you are aggregating as a fixed size (`size`). See Preserving the MIME types of the Aggregated Records. To learn about record processing within this component, see batch aggregation information in Process Phase.

Note that some connectors, such as Anypoint Connector for Salesforce (Salesforce Connector) and Anypoint Connector for NetSuite (NetSuite Connector), provide operations that can handle record-level errors without causing the batch aggregation process to fail.

When using Batch Aggregators, consider the following limitations:

- When using a Batch Aggregator component, do not attempt to process Guava data types, such as `ImmutableMap`. Instead, use a Java `Map` to avoid serialization issues.

- The Batch Aggregator component does not support job-instance-wide transactions. Within a Batch Step component, you can define a transaction that processes each record in a separate transaction. However, any transaction started by a Batch Step component ends before the Batch Aggregator component starts processing. Components cannot share a transaction because a transaction cannot cross the boundary between the components.

The following table describes each field and includes the XML element for the field.

| Field Name | XML | Description |
|---|---|---|
| Display Name | `doc:name` | Configurable name for the component. Example: `doc:name="My Aggregator"`. The default name is `Batch Aggregator`. |
| Aggregator Size | `size` | Size of each array of records to process. There is no default size. The processor within the component must accept an array as input. The component continues pulling records from the batch stepping queue into arrays of the configured size until none are left. If the queue contains fewer records than the configured size, the component pulls those records into a smaller array for processing. You must set the Size (`size`) or Streaming (`streaming`) property but not both. When using this configuration, the component does not wait for the Batch Step component to finish processing all records in an instance or batch. Once the set number of records is available in the stepping queue, the Batch Aggregator component pulls those records into an array and processes them. |
| Streaming | `streaming` | When `streaming=true`, the component acts on all records in a batch job instance and returns the results in an array of a size equal to the number of records in the instance. The batch size setting through the Batch Job component does not limit the number of records to process or return in the array. For example, assume that the aggregator returns the numeric IDs of a small batch job instance that processes only _ten_ records of the form `{"id": 1}`, `{"id": 2}`, and so on. In this case, the output array for the instance contains ten IDs, such as `[1, 6, 2, 7, 3, 8, 4, 9, 5, 10]`, even if the `blockSize` on the Batch Job component is set to a number smaller than the number of records in the instance, such as `5`. Processors can gain sequential access to the array of streamed records. Random access to the streamed records is not allowed because the aggregator does not preserve the processed records. There is no default. You must set the Size (`size`) or Streaming (`streaming`) property but not both. |
| Preserve Mime Types | `preserveMimeTypes` | Defaults to `false`. To preserve the MIME type of records processed within this component, set this attribute to `true`.  Processors that cannot determine the MIME type of data return output, such as `null`, or unreadable references to the payload, such as `[[B@e596d5c, [B@1c4c3b32], ...]`. Setting `preserveMimeTypes=true` is useful when this component is set to process a fixed number (`size`) of records. |

When deciding whether to stream aggregated records, consider the following:

- SaaS providers often have restrictions on accepting streaming input.

- Batch streaming is often useful in batch processing when writing to a file such as CSV, JSON, or XML.

- Batch streaming affects the performance of your application because the array of records is stored in RAM, which can slow the pace of transaction processing. Though performance slows, the trade-off of streaming data can warrant its use.

- Streaming prevents random access to records because a streaming commit is a one-read, forward-only iterator. However, you can perform random access operations when streaming if you use a component like For Each. For Each provides a separate array of records, which is accessible through its `records` variable.

## Configuring Batch Components

You can set up and configure Mule batch processing components to perform common batch processing use cases and to enhance the performance of batch jobs for cases in which the defaults require adjustment.

### Filtering Records to Process within a Batch Step Component

You can apply one or more record filters as attributes to any number of Batch Step components. For example, assume that the first Batch Step component within a given Batch Job component checks for a Salesforce contact in each record and the second updates the contact information in those records. To ensure that the second Batch Step processes only records that succeeded in the first step, you can configure a filter on the second Batch Step. The filter streamlines processing so that Mule focuses on only the relevant data for a given step.

To filter records, the Batch Step component supports one `acceptExpression` and one `acceptPolicy`. Both are optional, and no other Mule components accept these filters. If you use both filters on the same component, Mule evaluates the filters in the following order:

1. Accept Policy: acceptPolicy
1. Accept Expression: acceptExpression

A Batch Step component that uses an `acceptExpression` attribute applies a DataWeave expression to each record that reaches the component and accepts a record for processing within the component only if the expression evaluates to `true` for that record. If the record evaluates to `false`, the Batch Step component skips the record, and that record becomes available to the next Batch Step component within the Batch Job component if one exists.

The example below filters out all records in which the `age` value is less than `21`:

```xml
<batch:job jobName="batchJob">
  <batch:process-records >
    <batch:step name="adultsOnlyStep" acceptExpression="#[payload.age > 21]">
      ...
    </batch:step>
  </batch:process-records>
</batch:job>
```

A Batch Step component uses an `acceptPolicy` attribute to apply a policy to records processed in a previous Batch Step component. The Batch Step accepts a record for processing within the component only if the policy evaluates to `true` for that record. The default policy is `NO_FAILURES`. Other policies are `ONLY_FAILURES` and `ALL`. For descriptions of these policies, see Batch Step Component (<batch:step/>).

In the following example, the second Batch Step component (`batchStep2`) accepts only those records that failed to process successfully during the preceding step (`batchStep1`). For example, assume processors within `batchStep1` check each record for a Salesforce contact. If the check fails to find a contact, `batchStep2` accepts only those records without contacts, skipping records with contacts. Message processors within `batchStep2` can add a contact to those records.

```xml
<batch:job jobName="batchJob">
  <batch:process-records >
	  <batch:step name="batchStep1" >
      <!-- Check for contact -->
		  ...
    </batch:step>
    <batch:step name="batchStep2" accept-policy="ONLY_FAILURES">
      <!-- Accept records that failed -->
		  ...
    </batch:step>
  </batch:process-records>
</batch:job>
```

For demonstration purposes, the following example uses the Raise Error component (`<raise-error />`) to produce failures in the first Batch Step (`batchStep1`). The second Batch Step (`batchStep2`) accepts failed records only (`ONLY_FAILURES`) and logs the payload of those records. The third uses the default `acceptPolicy` to accept `NO_FAILURES`.

```xml
<flow name="batch-exampleFlow" >
  <scheduler doc:name="Scheduler" >
    <scheduling-strategy >
      <fixed-frequency frequency="75" timeUnit="SECONDS"/>
    </scheduling-strategy>
  </scheduler>
  <!-- Set Payload -->
  <set-payload value="#[[1,2,3,4,5]]" doc:name="Set Payload" />
  <!-- Batch Job Component -->
  <batch:job jobName="Batch_Job" maxFailedRecords="-1">
    <batch:process-records >
      <!-- First Batch Step defaults to NO_FAILURES -->
      <batch:step name="batchStep1" acceptPolicy="ALL"
                  acceptExpression="#[payload < 3]">
        <!-- Raising Error -->
        <raise-error doc:name="Raise error"
                     type="MY:APP" description="Example: Raising Error "/>
      </batch:step>
      <!-- Second Batch Step: ONLY FAILURES -->
      <batch:step name="batchStep2" acceptPolicy="ONLY_FAILURES">
        <logger level="INFO" doc:name="Logger" message="#[payload]"
                category="LOGGER IN SECOND BATCH STEP"/>
      </batch:step>
      <batch:step name="batchStep3" >
        <logger level="INFO" doc:name="Logger" message="#[payload]"
                category="LOGS IN THIRD BATCH STEP"/>
      </batch:step>
    </batch:process-records>
  </batch:job>
</flow>
```

- The Set Payload component (`<set-payload />`) sends the array `[1,2,3,4,5]` to the Batch Job component.
- The Batch Job component (`<batch:job />`) sets `maxFailedRecords` to `-1` so that failed records within the first Batch Step component do not stop the batch job instance from processing.
- The first Batch Step (`batchStep1`) configures `acceptExpression="#[payload < 3]"` to accept only records with a payload less than `3` and throws an error on those records because of the Raise Error component within it:
```text
INFO  ...DefaultBatchStep: Found error processing record on step 'batchStep1' for job instance 'f9bb6d60-5ef2-11ed-81e7-147ddaaf4f97'
of job 'batch-example-policiesBatch_Job'.
```

- The second Batch Step (`batchStep2`) prints the payload of the failed records, for example:
```text
INFO  ... LOGGER IN SECOND BATCH STEP: 1
INFO  ... LOGGER IN SECOND BATCH STEP: 2
```

- The third Batch Step (`batchStep3`) prints the payload of the successful records, for example:
```text
INFO ... LOGS IN THIRD BATCH STEP: 3
INFO  ...LOGS IN THIRD BATCH STEP: 4
INFO  ...LOGS IN THIRD BATCH STEP: 5
```

- After the batch job instance completes, the logs indicate that `3` records processed successfully and `2` records failed:
```text
INFO  ...engine.DefaultBatchEngine: Finished execution for instance ...
Total Records processed: 5. Successful records: 3. Failed Records: 2
```

For more information, see batch error handling faq.

### Performing Bulk Operations from a Batch Aggregator Component

Aggregation is useful for sending multiple records within an array to an external server. Within the Batch Aggregator component, you can add an operation, such as a bulk upsert, insert, or update operation, to load multiple records to a server with a single execution of an operation, instead of running an operation separately on each record.

You can process records in separate arrays of a fixed size or stream a single array of records from the batch job instance. For example, you can configure an Upsert operation in the Anypoint Connector for Salesforce (Salesforce Connector) to upsert 200 processed records. Alternatively, you can stream all the records in the instance to the server.

The following example bulk upserts records in separate arrays of 200 records per upsert:

```xml
<batch:job jobName="batchJob">
  <batch:process-records >
    <batch:step name="batchStep">
      <batch:aggregator size="200">
        <salesforce:upsert doc:name="Upsert" ... />
      </batch:aggregator>
    </batch:step>
  </batch:process-records>
</batch:job>
```

The following example streams upserts to a database:

```xml
<batch:job jobName="batchJob">
	<batch:process-records >
		<batch:step name="batchStep">
		  <batch:aggregator streaming="true">
		    salesforce:upsert doc:name="Upsert" ... />
		  </batch:aggregator>
		</batch:step>
	</batch:process-records>
</batch:job>
```

Error handling: +
Some connectors handle record-level errors without causing an entire batch aggregation process to fail, for example, Anypoint Connector for Salesforce (Salesforce Connector) and Anypoint Connector for NetSuite (NetSuite Connector). At runtime, these connectors keep track of records that the target resource accepts successfully and which fail. Rather than failing the entire group of records, the connector upserts as many records as it can and tracks any failures for notification purposes.

To learn more about processing within the Batch Aggregator component and how aggregation differs from processing within the Batch Step component, see Process Phase.

### Modifying Records within a Batch Aggregator

You can modify records within the Batch Aggregator component, just as you can modify them with processors in the Batch Step component. The modifications can take place sequentially or through random access to specific records.

#### Sequential Processing within a Batch Aggregator

The following example performs sequential access to records. Using Groovy within a Scripting module, the example modifies the payload of each record from the For Each component's iteration and creates a variable for each collected record.

```xml
<batch:job jobName="batchJob">
  <batch:process-records>
    <batch:step name="batchStep">
      <batch:aggregator doc:name="batchAggregator" size="10">
        <foreach doc:name="For Each">
          <script:execute engine="groovy">
            <script:code>
	      vars['marco'] = 'polo'
	      vars['record'].payload = 'hello'
	    </script:code>
	  </script:execute>
        </foreach>
      </batch:aggregator>
    </batch:step>
  </batch:process-records>
</batch:job>
```

#### Randomly Accessing Records within a Batch Aggregator

You can also use the For Each scope when randomly accessing records by their iteration number. For Each exposes a `records` variable, which is an immutable list that it uses to keep track of the iteration. You can use this variable to randomly access records in the list from the Batch Aggregator component.

To demonstrate random access when using fixed-size aggregation, the following example specifies the index of a record in the For Each list of records. Instead of sequentially accessing each record, using the `records` variable with an index of a record selects a single record from the list. The example uses the Scripting module to modify the payload of the selected record and create a variable for that record:

```xml
<batch:job jobName="batchJob">
  <batch:process-records>
    <batch:step name="batchStep">
      <batch:aggregator doc:name="batchAggregator" size="10">
        <foreach doc:name="For Each">
	  <script:execute engine="groovy">
	    <script:code>
	      records[0].vars['marco'] = 'polo'
	      records[0].vars['record'].payload = 'hello'
	    </script:code>
	  </script:execute>
	</foreach>
      </batch:aggregator>
    </batch:step>
  </batch:process-records>
</batch:job>
```

You can configure a Batch Aggregator component to stream its content. Setting this component to stream the records (`streaming="true"`) enables you to process an array of all the records in the batch job instance without running out of memory, regardless of how many or how large the records are. For example, if you need to write millions of records to a CSV file, you can stream the records with the Batch Aggregator component.

```xml
<batch:job jobName="batchJob">
  <batch:process-records >
    <batch:step name="batchStep">
      <batch:aggregator streaming="true">
        <file:write path="reallyLarge.csv">
	  <file:content><![CDATA[%dw 2.0
	    ...

	  }]]></file:content>
      </batch:aggregator>
    </batch:step>
  </batch:process-records>
</batch:job>
```

As the following example shows, only sequential access to records is possible when streaming within the Batch Aggregator component. Random access is not supported when streaming because streaming requires access to the entire set of records. This restriction is necessary because Mule cannot guarantee that all records will fit in memory if no fixed size is specified.

```xml
<batch:job jobName="batchJob">
  <batch:process-records>
    <batch:step name="batchStep">
      <batch:aggregator doc:name="batchAggregator" streaming="true">
        <foreach doc:name="For Each">
	  <script:execute engine="groovy">
	    <script:code>
	      vars['marco'] = 'polo'
	      vars['record'].payload = 'foo'
	    </script:code>
	  </script:execute>
	</foreach>
      </batch:aggregator>
    </batch:step>
  </batch:process-records>
</batch:job>
```

To learn more about processing within the Batch Aggregator component and how aggregation differs from processing within the Batch Step component, see Process Phase.

> **Note:** :

When using a Batch Aggregator component, do not attempt to process Guava data types, such as `ImmutableMap`. Instead, use a Java Map to avoid serialization issues.

### Preserving the MIME types of the Aggregated Records

_Introduced in Mule 4.3_

Aggregated records pass into the Batch Aggregator component as an array containing each record’s payload. However, by default, the MIME types associated with those payloads are not preserved. To preserve record’s MIME types, specify the `preserveMimeTypes` attribute in the Batch Aggregator component.

Consider the following JSON array:

```json
[
  {
    "name": "Tony Stark",
    "alias": "Iron Man",
    "status": "DEAD"
  },
  {
    "name": "Steve Rodgers",
    "alias": "Captain America",
    "status": "RETIRED"
  },
  {
    "name": "Peter Parker",
    "alias": "SpiderMan",
    "status": "FUGITIVE"
  }
]
```

Assume that the JSON array is the input to the following Batch Job component:

```xml
<batch:job name="avengersLogger">
  <batch:process-records>
    <batch:step name="log">
      <batch:aggregator size="10">
        <foreach>
	  <logger message="Agent #[payload.alias] is #[payload.status]" />
	</foreach>
      </batch:aggregator>
    </batch:step>
  </batch:process-records>
</batch:job>
```

The batch engine splits the input JSON array into individual records, which  aggregator block receives an array with three elements. The first one of them is:

```json
{
  "name": "Tony Stark",
  "alias": "Iron Man",
  "status": "DEAD"
}
```

However, when the Logger component attempts to evaluate the `#[payload.alias]` expression, an error similar to the following one results:

```text
********************************************************************************
Message               : "You called the function 'Value Selector' with these arguments:
  1: Binary ("ewogICJmaXJzdE5hbWUiOiAiUmFtIiwKICAibGFzdE5hbWUiOiAiUmFtMSIsCiAgImFkZHJlc3Mi...)
  2: Name ("alias")

But it expects one of these combinations:
  (Array, Name)
  (Array, String)
  (Date, Name)
  (DateTime, Name)
  (LocalDateTime, Name)
  (LocalTime, Name)
  (Object, Name)
  (Object, String)
  (Period, Name)
  (Time, Name)

5|                                         name: payload.alias,
                                                 ^^^^^^^^^^^^^
```

This error occurs because MIME types are not preserved, which prevents Mule from reading it as JSON. To resolve this issue, you must set the `preserveMimeTypes` attribute in the Batch Aggregator component to `true`, for example:

```xml
<batch:aggregator size="10" preserveMimeTypes="true">
  <foreach>
    <logger message="Agent #[payload.alias] is #[payload.status]" />
  </foreach>
</batch:aggregator>
```

The setting makes Mule maintain each record's media type and treat the payload as a JSON document.

### Changing the Record Block Size

A traditional online processing model typically maps each request to a worker thread. Generally, there is 1:1 relationship between a request and a running thread regardless of the processing type. This relationship holds for synchronous, asynchronous, one-way, and request-response processing types, and when temporarily buffering requests before processing.

However, in a batch job, the traditional threading model does not apply because records are first stored in a persistent queue, before the Process phase begins.

To improve performance, Mule runtime queues and schedules batch records in blocks
of up to 100 records per thread. This behavior reduces the number of I/O requests
and improves an operation's load. Batch jobs use Mule thread pools, so there is no default for the job. Each thread iterates through that block to
process each record, and then each block is queued back, and the process continues.

Consider having 1 million records to place in a queue for a 3-step batch job. At least three million I/O operations occur as the Mule runtime engine takes and requests each record as they move through the job's phases. +
Performance requires having enough available memory to process the threads in parallel, which means moving the records from persistent storage into RAM. The larger your records and their quantity, the more available memory you need for batch processing.

Although the standard model of up to 100 records per thread in the batch job works for most use cases, consider three use cases where you need to increase or decrease the block size:

- Assume you have 200 records to process through a batch job. With the default 100-record block size, Mule can only process two records in parallel at a time. If a batch job has fewer than 101 records to process, then processing becomes sequential. If you need to process heavy payloads, then queueing a hundred records demands a large amount of working memory.
- Consider a batch job that needs to process images, and an average image size of 3 MB. In this case, Mule processes 100-record blocks with payloads of 3 MB in each thread. Hence, your default threading-profile setting would require a large amount of working memory just to keep the blocks in the queue. In this case, set a lower block size to distribute each payload through more jobs and lessen the load on your available memory.
- Suppose you have 5 million records with payloads so small that you can fit blocks of 500 records in your memory without problems. Setting a larger block size improves your batch job time without sacrificing working memory load.

To take full advantage of this feature, you must understand how the block sizes affect your batch job. Running comparative tests with different values and testing performance helps you find an optimum block size before moving this change into production.

Remember that modifying the batch block size is optional. If you apply no changes, the default value is 100 records per block.

You set the size through the Batch Job component, for example:

```xml
<batch:job jobName="atch_Job" blockSize="200">
  ...
</batch:job>
```

### Setting a Max Concurrency Limit on Batch Job Instances

The Max Concurrency (`maxConcurrency`) property limits the number of record blocks to process concurrently.

You can configure the `maxConcurrency` property as in the following example:

```xml
<batch:job jobName="test-batch" maxConcurrency="${batch.max.concurrency}">
  ...
</batch:job>
```

By default, the Batch Job component limits the maximum concurrency to twice the number of available cores. The capacity of the system running the Mule instance also limits concurrency.

## Batch Errors

When a Mule app processes records through batch steps, record-level failures result in a `BatchError` object associated with the failed record. You can use DataWeave functions and selector expressions to inspect error details such as description, type, and stack trace. Starting with Mule 4.11, batch record errors replace exception-based tracking and wrap Mule error objects with enhanced error data.

### Accessing Batch Errors

Within a batch step, you can access record errors using these DataWeave functions:

| DataWeave Function | Description |
|---|---|
| `#[Batch::failureErrorForStep(String)]` | Receives the name of a step as a String argument. Returns the `BatchError` object if the current record failed on that step. Otherwise, returns `null`. |
| `#[Batch::getStepErrors()]` | Returns a `Map<String, BatchError>` where keys are batch step names where the current record failed, and values are the corresponding errors. + If the record hasn't failed in any step, returns an empty map (never `null`). The map doesn't contain entries for steps in which the record hasn't failed. |
| `#[Batch::getFirstError()]` | Returns the `BatchError` object for the first step in which the current record has failed. If the record hasn't failed in any step, returns `null`. |
| `#[Batch::getLastError()]` | Returns the `BatchError` object for the last step in which the current record failed. Otherwise, returns `null`. |

### Selector Expressions for Batch Errors

Batch errors are complex data types with several fields, such as a description and type. When logging and handling batch errors, you can select values from any of these fields. This table shows selector expressions for the first step in which the current record failed:

| Field | Description | Selector Expression |
|---|---|---|
| Description | A description of the problem. | `#[Batch::getFirstError().description]` |
| Detailed Description | A description of the problem, which can be the same or more extensive than the description field. | `#[Batch::getFirstError().detailedDescription]` |
| Type | A type that characterizes the problem and allows for routing within an error handler. | `#[Batch::getFirstError().errorType]` |
| Failing Component | The component where the error is generated. | `#[Batch::getFirstError().failingComponent]` |
| DSL Source | The DSL source of the component where the error is generated. | `#[Batch::getFirstError().dslSource]` |
| Error Message | An optional Mule message with error data (for example, HTTP response content for invalid status codes). | `#[Batch::getFirstError().errorMessage]` |
| Child Errors | An optional collection of inner errors, used by elements like Scatter-Gather to provide aggregated route errors. | `#[Batch::getFirstError().childErrors]` |
| Failure During Handling | Any error that occurs while handling this error. | `#[Batch::getFirstError().failureDuringHandling]` |
| Stack Trace | The Java stack trace of the exception. | `#[Batch::getFirstError().stackTrace]` |

### Batch Error Types

Batch errors follow the same error type hierarchy as standard Mule errors. A special `MULE:BATCH` error type exists for errors that arise during internal batch processing (rather than chain execution) and don't belong to any specific type.

## Handling Errors During Batch Job

Handle record-level failures in Mule batch jobs while balancing logging detail and performance. Learn how batch steps log errors, how failed records propagate through a job, and how to inspect errors by using DataWeave functions.

Batch jobs capture record-level failures during batch step execution. For details about the error representation and how to access error fields, see Batch Errors.

Mule batch processing is designed to handle large data sets and to perform almost real-time data integration that recovers from crashes and continues processing a job from a point of failure. However, _verbose_ logs for issues that occur in large data sets can become enormous and severely impact performance.

To limit this impact, Mule uses INFO-level logging by default, as described in default logging. For cases in which you require more verbose log messages, you can change the mode to DEBUG. This mode is helpful for debugging and is feasible for some cases that involve smaller data sets.

Set the logging mode with this property:

```xml
<AsyncLogger name="com.mulesoft.mule.runtime.module.batch" level="DEBUG" />
```

If you're using CloudHub or Runtime Manager, you can add this package to the Logs tab in DEBUG level:

```text
com.mulesoft.mule.runtime.module.batch
```

Avoid using the DEBUG mode in a production environment when processing large data sets.

Starting with Mule 4.11, batch error handling relies on `BatchError` objects instead of exceptions.

### Logs of Failing Records Inside a Batch Step

When processing a batch job instance, a processor inside a batch step can fail or raise an error, for example, because of corrupted or incomplete record data. By default, Mule uses the INFO log level to log stack traces according to this logic when issues occur:

1. Mule gets the exception's full stack trace.
1. Mule strips the stack trace from error messages in the log.
Even if all records raise the same error, the messages being processed would probably contain specific information related to those records. For example, if you push leads to a Salesforce account and one record fails because the lead was uploaded, another repeated lead would have different record information, but the error is the same.
1. Mule verifies if the stack trace was already logged in the current step.
The first time the runtime encounters this error, Mule logs the error and produces a message like this one:
```text
com.mulesoft.mule.runtime.module.batch.internal.DefaultBatchStep:
Found error processing record on step 'batchStep1'
for job instance 'Batch Job Example' of job 'CreateLeadsBatch'.

This is the first record to show this error on this step
for this job instance. Subsequent records with the same failures
will not be logged for performance and log readability reasons:
```

Mule logs on a "by step" basis. If another step also raises the same error, the runtime logs it again for that step.
1. When the batch job reaches the On Complete phase, Mule displays an error summary with every error type and the number of occurrences in each batch step. +
The error summary for a batch job with two batch steps that raised an `APP:FAILURE` error:
```text
*******************************************************************************
* - - + Error Type + - - * - - + Step + - - * - - + Count + - - *
*******************************************************************************
* APP:FAILURE * batchStep1 * 10 *
* APP:FAILURE * batchStep2 * 9 *
*******************************************************************************
```

Here, the first step failed ten times and the second failed nine.

Mule logs batch errors using this behavior as its default configuration, which only logs INFO level messages to get a balanced trade-off between logging efficiency for large chunks of data. +
However, your motivation to use batch processing might not be its ability to handle large datasets, but its capacity to recover from a crash and keep processing a batch job from where it was left off when performing "near real-time" data integration. Or you may need more verbose log levels for debugging. +

### DataWeave Functions for Error Handling

Mule 4.x includes a set of DataWeave functions that you can use in the context of a batch step.

| DataWeave Function | Description |
|---|---|
| `#[Batch::isSuccessfulRecord()]` | A boolean function that returns true if the current record hasn't presented errors in any prior step. |
| `#[Batch::isFailedRecord()]` | A boolean function that returns true if the current record has presented errors in any prior step. |
| `#[Batch::failureErrorForStep(String)]` | Receives the name of a step as a String argument. If the current record presented an error on that step, it returns the `BatchError` object. Otherwise, returns `null`. |
| `#[Batch::getStepErrors()]` | Returns a `Map<String, BatchError>` in which the keys are the name of a batch step in which the current record has failed, and the value is the error itself. + If the record hasn't failed in any step, this map is empty but never `null`. The map contains no entries for steps in which the record hasn't failed. |
| `#[Batch::getFirstError()]` | Returns the `BatchError` for the first step in which the current record has failed. If the record hasn't failed in any step, returns `null`. |
| `#[Batch::getLastError()]` | Returns the `BatchError` for the last step in which the current record has failed. If the record hasn't failed in any step, returns `null`. |

There are also bindings to work with the old batch error handling mechanism, which relied on exceptions rather than `BatchError` objects.

| DataWeave Function | Description |
|---|---|
| `#[Batch::failureExceptionForStep(String)]` | Receives the name of a step as a String argument. If the current record throws an exception on that step, it returns the Exception object. Otherwise, returns `null`. |
| `#[Batch::getStepExceptions()]` | Returns a Java `Map<String, Exception>` in which the keys are the name of a batch step in which the current record has failed, and the value is the exception itself. + If the record hasn't failed in any step, this map is empty but never `null`. The map contains no entries for steps in which the record hasn't failed. |
| `#[Batch::getFirstException()]` | Returns the Exception for the first step in which the current record has failed. If the record hasn't failed in any step, returns `null`. |
| `#[Batch::getLastException()]` | Returns the Exception for the last step in which the current record has failed. If the record hasn't failed in any step, returns `null`. |

#### Example

Consider a batch job that polls files containing contact information:

- In the first step, the batch job aggregates the contact information and transforms it using the Transform Message component, then pushes the data to Salesforce.
- In the second step, the job transforms the same contacts again to match the data structure of another third-party contacts application (such as Google Contacts) and pushes them to this service using an HTTP request.
- In the third step, you write into a JMS dead-letter queue for each record that has failed. The message content is the error itself. Each record could have failed in both steps, meaning the same record translates into two JMS messages.

Such an application would look like this:

Since the goal is to gather failures, it makes sense to configure the `Failures` step with an ONLY_FAILURES filter (see batch filters and batch aggregator for more details about batch filters).
The set-payload processor in this step can be configured to use the `Batch::getStepErrors()` function.

This function returns a map with all errors found in all steps. To send the errors through JMS, use a For Each scope to iterate over the map's values (the errors) and send them through a JMS outbound endpoint:

### Batch Processing Strategies for Error Handling

Mule has three options for handling a record-level error:

1. **Finish processing** Stop the execution of the current job instance. Finish the execution of the records currently in-flight, but do not pull any more records from the queues and set the job instance into a `FAILURE` state. The On Complete phase is invoked.
1. **Continue processing** the batch regardless of any failed records, using the `acceptExpression` and `acceptPolicy` attributes to instruct subsequent batch steps how to handle failed records.
1. **Continue processing** the batch regardless of any failed records (using the `acceptExpression` and `acceptPolicy` attributes to instruct subsequent batch steps how to handle failed records), until the batch job accumulates a **maximum number of failed records** at which point the execution will halt just like in option 1.

By default, Mule batch jobs follow the first error handling strategy, which halts the batch instance execution. This behavior is controlled through the `maxFailedRecords` attribute.

| Failed Record Handling Option | Batch Job Attribute | Value |
|---|---|---|
| Stops processing when a failed record is found | `maxFailedRecords` | `0` |
| Continues processing indefinitely, regardless of the number of failed records | `maxFailedRecords` | `-1` |
| Continues processing until reaching the maximum number of failed records | `maxFailedRecords` | `integer` |

```xml
<batch:job jobName="Batch1" maxFailedRecords="0">
```

#### Crossing the Max Failed Threshold

When a batch job accumulates enough failed records to cross the `maxFailedRecords` threshold, Mule aborts processing for any remaining batch steps, skipping directly to the On Complete phase.

For example, if you set the value of `maxFailedRecords` to "10" and a batch job accumulates ten failed records in the first of three batch steps, Mule does not attempt to process the batch through the remaining two batch steps. Instead, it aborts further processing and skips directly to On Complete to report on the batch job failure.

If a batch job _does not_ accumulate enough failed records to cross the `maxFailedRecords` threshold, _all_ records – successes and failures – continue to flow from batch step to batch step; use filters to control which records each batch step processes.

## Batch Job Instance ID

Users of batch processing frequently need the ability to determine a Batch job's instance ID during the execution phases of a Batch job.

The Batch job instance ID is useful to:

- Pass the local job instance ID to an external system for referencing and managing data
- Improve the job’s custom logging
- Send email or SMS notifications for meaningful events

### Example

Mule exposes the batch job instance ID through a flow variable of key `batchJobInstanceId`. That flow variable is available at the beginning of the input phase. The flow variable is also available in every step and in the on-complete phase.

The log output produces the following:

```text
com.mulesoft.mule.runtime.module.batch.internal.engine.DefaultBatchEngine: Created instance '7dc5cad0-ab09-11e8-a790-9801a7b055d3' for batch job 'CreateLeadsBatch'
```

### Custom Batch Job Instance ID

You can use a DataWeave expression to specify a unique identifier for each batch job by passing a **Job Instance Id** attribute that takes a DW expression. +
Note that constant values are not allowed for batch jobs and if the DW expression returns a previously seen value, Mule throws an exception and does not create the job instance.
If you don't set a job instance ID, Mule auto generates a UUID to assign to your instance.

The UUID generated for the job instance described above is `ba01e1a0-f5c7-11e4-9414-10ddb1daeb6d`. As you can tell, it's not a human readable identifier making it hard to correlate to an actual execution and considering you could be running multiple jobs at the same time, this ID is not meaningful at all.

To guarantee uniqueness, you can define the Job Id as the server's current date by using the following DataWeave expression: +
`#['Job From ' ++ now() as String {format: 'dd/MM/yy hh:mm:ss'}]`.

This names the execution instance `Job From 15/01/16 05:23:12`.

```text
com.mulesoft.module.batch.engine.DefaultBatchEngine: Created instance Job From 15/01/16 05:23:12 for batch job contacts-to-SFDCBatch
com.mulesoft.module.batch.engine.DefaultBatchEngine: Starting input phase
com.mulesoft.module.batch.engine.DefaultBatchEngine: Input phase completed
com.mulesoft.module.batch.engine.queue.BatchQueueLoader: Starting loading phase for instance 'Job From 15/01/16 05:23:12' of job 'contacts-to-SFDCBatch'
com.mulesoft.module.batch.engine.queue.BatchQueueLoader: Finished loading phase for instance Job From 15/01/16 05:23:12 of job contacts-to-SFDCBatch. 3 records were loaded
com.mulesoft.module.batch.engine.DefaultBatchEngine: Started execution of instance 'Job From 15/01/16 05:23:12' of job 'contacts-to-SFDCBatch'
```

The logs of a properly identified instance are easier to read.

```xml
<batch:job jobName="CreateLeadsBatch" maxFailedRecords="1000" jobInstanceId="#['Job From ' ++ now() as String {format: 'dd/MM/yy hh:mm:ss'}]">
	<batch:process-records >
		<batch:step name="LeadExistsStep">
			...
		</batch:step>

		<batch:step name="LeadInsertStep" acceptExpression="vars.leadNotFound">
			...
		</batch:step>
	</batch:process-records>
	<batch:on-complete >
		...
	</batch:on-complete>
</batch:job>
```
