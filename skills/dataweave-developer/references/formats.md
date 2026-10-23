# DataWeave data formats

Supported MIME types with their reader and writer properties.

## Supported Data Formats

DataWeave can read and write many types of data formats, such as JSON, XML, and
many others.

DataWeave supports the following formats as input and output:

| MIME Type | ID | Supported Formats |
|---|---|---|
| `application/avro` | `avro` | Avro Format |
| `application/csv` | `csv` | CSV Format |
| `application/dw` | `dw` | DataWeave Format (dw) for testing a DataWeave expression |
| `application/flatfile` | `flatfile` | Flat File Format, COBOL Copybook Format, Fixed Width Format |
| `application/java` | `java` | Java Format, Enum Format for Java |
| `application/json` | `json` | JSON Format |
| `application/octet-stream` | `binary` | Binary Format |
| `application/protobuf`, `application/x-protobuf` | `protobuf` | Protobuf Format |
| `application/xlsx` | `excel` | Excel Format |
| `application/xml` | `xml` | XML Format, CData Custom Type |
| `application/x-ndjson` | `ndjson` | Newline Delimited JSON Format (ndjson) |
| `application/x-www-form-urlencoded` | `urlencoded` | URL Encoded Format |
| `application/yaml` | `yaml` | YAML Format |
| `multipart/form-data` | `multipart` | Multipart Format |
| `text/plain` | `text` | Text Plain Format |
| `text/x-java-properties` | `properties` | Text Java Properties |

### DataWeave Readers

DataWeave can read input data as a whole by loading it into memory or by indexing it in local storage and, for some data formats, DataWeave can read data sequentially in parts by streaming the input. The indexed reading strategy implements a mechanism to avoid out-of-memory issues when processing large files. The streaming strategy can improve performance but restricts file access to sequential access (which disallows random access) because you can access only the part of the file that is being read and stored in memory.

| Read Strategy | Description | Supported Formats <.^| In-Memory |
|---|---|---|
| This strategy parses the entire document and loads it into memory, enabling random access to data. When using this strategy, a DataWeave script can access any part of the resulting value at any time. | DataWeave can read all supported formats using this strategy. <.^\| Indexed | This strategy parses the entire document and uses disk space to avoid out-of-memory issues on large files, enabling random access to data. When using this strategy, a DataWeave script can access any part of the resulting value at any time. When processing a `String` with a size larger than 1.5 MB, DataWeave automatically splits the value in chunks to avoid out-of-memory issues. This feature works only with `JSON` and `XML` input data. For additional details, see Indexed Readers in DataWeave |
|  · `CSV` · `JSON` · `XML` <.^\| Streaming | This strategy partitions the input document into smaller items and accesses the data sequentially, storing the current item in memory. A DataWeave selector can access only the portion of the file that is getting read. For additional details, see Streaming in DataWeave |  · `CSV` · `JSON` · `Excel` (XLSX) · `XML` |

### Using Reader and Writer Properties

In some cases, it is necessary to modify or specify aspects of the format
through format-specific properties. For example, you can specify CSV input and
output properties, such as the `separator` (or delimiter) to use in the CSV file.
For Cobol copybook, you need to specify the path to a schema file using the
`schemaPath` property.

You can append reader properties to the MIME type (`outputMimeType`) attribute
for certain components in your Mule app. Listeners and Read operations accept
these settings. For example, this On New File listener example identifies the `,` separator for a CSV input file:

**Example: Properties for the CSV Reader**

```xml
<file:listener doc:name="On New File" config-ref="File_Config" outputMimeType='application/csv; separator=","'>
  <scheduling-strategy >
    <fixed-frequency frequency="45" timeUnit="SECONDS"/>
  </scheduling-strategy>
  <file:matcher filenamePattern="comma_separated.csv" />
</file:listener>
```

Note that the `outputMimeType` setting above helps the CSV _reader_ interpret
the format and delimiter of the input `comma_separated.csv` file, not the writer.

To specify the output format, you can provide the MIME type and any writer
properties for the writer, such as the CSV or JSON writer used by a File Write
operation. For example, you might need to write a pipe (`|`) delimiter in your
CSV output payload, instead of some other delimiter used in the input. To do
this, you append the property and its value to the `output` directive of a
DataWeave expression. For example, this Write operation specifies the pipe as
a `separator`:

**Example: output Directive for the CSV Writer**

```xml
<file:write doc:name="Write" config-ref="File_Config" path="my_transform">
  <file:content ><![CDATA[#[output application/csv separator="|" --- payload]]]></file:content>
</file:write>
```

The following example shows a DataWeave script in which the `output` directive specifies two writer properties, one for the CSV field separator, another to indicate that there is no header.

```json
%dw 2.0
output application/csv separator=";", header=false
---
payload
```

Writer properties depend on the format. The following example uses the JSON writer property, `skipNullOn`:

```json
%dw 2.0
output application/json skipNullOn="everywhere"
---
payload
```

The following example shows a DataWeave script that uses an invisible ASCII character as a separator for the CSV output. The separator property value is `\u001E`. `\u` is the escape sequence representation and `001E` is the hexadecimal representation of the record separator (RS) ASCII character.

```dataweave
%dw 2.0
output application/csv separator = "\u001E"
---
[
	{
		"Name" : "Tom",
		"UID" : 2569,
		"ShipOrderID" : "ui-288188"
	},
	{
		"Name" : "Alan",
		"UID" : 7756,
		"ShipOrderID" : "xj-232142"
	},
	{
		"Name" : "Dan",
		"UID" : 7821,
		"ShipOrderID" : "uk-259459"
	}
]
```

The CSV example produces the following output:

```text
NameUIDShipOrderID
Tom2569ui-288188
Alan7756xj-232142
Dan7821uk-259459
```

Scripts that use the `read` or `readUrl` methods can also specify reader properties through the `readerProperties` parameter. See examples in read. However, note that use of reader properties is more common in message sources, such as the HTTP listener, as shown in the CSV reader example.

It is also possible to use a Mule variable as a value of a configuration property. For more complete examples, see Set Reader and Writer Configuration Properties.

### Setting MIME Types

You can specify the MIME type for the input and output data that flows through
a Mule app.

For DataWeave transformations, you can specify the MIME type for the output data.
For example, you might set the `output` header directive of an expression in the
Transform Message component or a Write operation to `output application/json` or
`output application/csv`.

This example sets the MIME type through a File Write operation to ensure that a
format-specific writer, the CSV writer, outputs the payload in CSV format:

**Example: MIME Type for the CSV Writer**

```xml
<file:write doc:name="Write" config-ref="File_Config" path="my_transform">
  <file:content ><![CDATA[#[output application/csv --- payload]]]></file:content>
</file:write>
```

Starting in Mule 4.3.0, you can set the `output` directive using the format ID alone,
instead of using the MIME type. For example, you might set the `output` header directive
of an expression in the Transform Message component or a Write operation to
`output json` or `output csv`. You can also use the format ID to
differentiate the format of the output data from the MIME type in the output header, and
you can use a custom MIME type.
For example, you can write JSON data but customize the MIME type to
`application/problem+json` by using the DataWeave directive `output application/problem+json with json`.
See Change a Script's MIME Type Output
for examples that customize the MIME type output of a script.

The `with` keyword separates the output MIME type from the DataWeave writer for the script's output. For example, you can specify 'output application/csv with binary' to output the `application/csv` MIME type when using the `binary` writer. This setting is necessary in cases shown in cookbook writer prop mule and Use Reader and Writer Properties in DataWeave Functions. It is also possible to append writer properties, such as in the use case `output application/my-custom-type with json indent=false`.

For input data, format-specific readers for Mule sources (such as the
On New File listener), Mule operations (such as Read and HTTP Request
operations), and DataWeave expressions attempt to infer the MIME type
from metadata that is associated with input payloads, attributes, and
variables in the Mule event. When the MIME type cannot be inferred from
the metadata (and when that metadata is not static), Mule sources and
operations allow you to specify the MIME type for the reader. For example,
you might set the MIME type for the On New File listener to
`outputMimeType='application/csv'` for CSV file _input_. This setting provides
information about the file format to the CSV reader.

**Example: MIME Type for the CSV Reader**

```xml
<file:listener doc:name="On New File"
  config-ref="File_Config"
  outputMimeType='application/csv'>
</file:listener>
```

Note that reader settings _are not_ used to perform a transformation from one
format to another. They simply help the reader interpret the format of the input.

You can also set special reader and writer properties for use by the
format-specific reader or writer of a source, operation, or component.
See reader writer properties.

### See Also

Transform Message Component

Flat File Schemas

---

## JSON Format

MIME type: `application/json`

ID: `json`

In the JSON data format, values map one-to-one with DataWeave values.
JSON supports `String`, `Boolean`, `Number`, `Null`, `Object`, and `Array` types. DataWeave supports each of these values natively.

The DataWeave reader for JSON input supports the following parsing strategies:

- Indexed
- In-Memory
- Streaming

To understand the parsing strategies that DataWeave readers and writers can apply to this format, see DataWeave Parsing Strategies.

### Examples

The following examples show uses of the JSON format:

- example1
- example2
- example3

#### Example: Represent JSON in the DataWeave (dw) Format

This example shows how JSON input is represented in the DataWeave (dw) format.

##### Input

The following JSON object serves as the input payload to the DataWeave source.

```json
{
  "name": "Matias",
  "age": 8,
  "male": true,
  "kids": null,
  "brothers": ["Pedro", "Sara"]
}
```

##### Source

The DataWeave script transforms the JSON input payload to the DataWeave (dw) format and MIME type.

```dataweave
output application/dw
---
payload
```

##### Output

Notice that only the keys of the JSON input and the `application/dw` output differ. The JSON keys are surrounded by quotation marks. These DataWeave (dw)
keys do not require quotation marks. See Valid Keys for details.

```dataweave
{
  name: "Matias",
  age: 8,
  male: true,
  kids: null,
  brothers: [
    "Pedro",
    "Sara"
  ]
}
```

#### Example: Convert Repeated XML Elements to JSON

This example shows how to convert repeated XML elements to JSON.

Note that XML encodes collections using repeated (unbounded) elements. DataWeave represents unbounded elements by repeating the same key.

##### Input

The following XML data contains repeating child elements with the
key `name`. This XML serves as the input payload to the DataWeave source.

```xml
<?xml version='1.0' encoding='UTF-8'?>
<friends>
  <name>Mariano</name>
  <name>Shoki</name>
  <name>Tomo</name>
  <name>Ana</name>
</friends>
```

##### Source

The following DataWeave script takes the XML input as its payload and outputs that payload in the JSON format.

The script selects the `name` elements from the XML input and uses the DataWeave `map` function to map the values of those elements into an array of objects. Each object in the array takes the form `{ name : item }`, where `item` is the value of the `name` element. The entire array serves as the value of the `friends` key.

```dataweave
%dw 2.0
output application/json
---
friends: payload.friends.*name map (
            (item, index) -> {name: item}
         )
```

##### Output

The DataWeave script outputs the following JSON object.

```json
{
  "friends": [
    {
      "name": "Mariano"
    },
    {
      "name": "Shoki"
    },
    {
      "name": "Tomo"
    },
    {
      "name": "Ana"
    }
  ]
}
```

#### Example: Stream JSON Data

To demonstrate streaming, the following example streams a JSON file by reading
each element in an array one at a time.

##### Input

The JSON input payload serves as input for the XML configuration.

**JSON Input (truncated):**

```json
{ "myJsonExample" : [
    {
      "name" : "Shoki",
      "zipcode": "95838"
    },
    {
      "name" : "Leandro",
      "zipcode": "95823"
    },
    {
      "name" : "Mariano",
      "zipcode": "95815"
    },
    {
      "name" : "Cristian",
      "zipcode": "95815"
    },
    {
      "name" : "Kevin",
      "zipcode": "95824"
    },
    {
      "name" : "Stanley",
      "zipcode": "95841"
    }
  ]
}
```

##### XML Configuration

The following XML configuration streams JSON input.

```xml
<file:config name="File_Config" doc:name="File Config" />
<flow name="dw-streaming-jsonFlow" >
  <scheduler doc:name="Scheduler" >
    <scheduling-strategy >
      <fixed-frequency frequency="1" timeUnit="MINUTES"/>
    </scheduling-strategy>
  </scheduler>
  <file:read doc:name="Read"
     config-ref="File_Config"
     path="${app.home}/myjsonarray.json"
     outputMimeType="application/json; streaming=true"/>
  <ee:transform doc:name="Transform Message" >
    <ee:message >
      <ee:set-payload ><![CDATA[%dw 2.0
output application/json
---
payload.myJsonExample map ((element) -> {
returnedElement : element.zipcode
})]]></ee:set-payload>
    </ee:message>
  </ee:transform>
  <file:write doc:name="Write"
    path="/path/to/output/file/output.json"
    config-ref="File_Config1"/>
  <logger level="INFO" doc:name="Logger" message="#[payload]"/>
</flow>
```

- The streaming example configures the File Read operation to stream the JSON input
by setting `outputMimeType="application/json; streaming=true"`.
In the Studio UI, you can set the **MIME Type** on the listener to `application/json`
and the **Parameters** for the MIME Type to **Key** `streaming` and **Value** `true`.
- The DataWeave script in the **Transform Message** component iterates over the
array in the input payload and selects its `zipcode` values.
- The Write operation returns a file, `output.json`, which contains the result
of the transformation.
- The Logger prints the same output payload that you see in `output.json`.

##### Output

The JSON streaming example produces a JSON array of objects.

```json
[
  {
    "returnedElement": "95838"
  },
  {
    "returnedElement": "95823"
  },
  {
    "returnedElement": "95815"
  },
  {
    "returnedElement": "95815"
  },
  {
    "returnedElement": "95824"
  },
  {
    "returnedElement": "95841"
  }
]
```

### Configuration Properties

DataWeave supports the following configuration properties for this format.

#### Reader Properties

This format accepts properties that provide instructions for reading input data.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `streaming` | `Boolean` | `false` | Streams input when set to `true`. Use only if entries are accessed sequentially. The input must be a top-level array. See the streaming example, and see DataWeave Readers. Valid values are `true` or `false`. |

#### Writer Properties

This format accepts properties that provide instructions for writing output data.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `bufferSize` | `Number` | `8192` | Size of the buffer writer, in bytes. The value must be greater than `8`. |
| `deferred` | `Boolean` | `false` | Generates the output as a data stream when set to `true`, and defers the script's execution until the generated content is consumed. Valid values are `true` or `false`. |
| `duplicateKeyAsArray` | `Boolean` | `false` | Converts the values of duplicate keys in an object to a single array of values to the duplicated key. Valid values are `true` or `false`. |
| `encoding` | `String` | `'UTF-8'` | The encoding to use for the output, such as UTF-8. |
| `indent` | `Boolean` | `true` | Write indented output for better readability by default, or compress output into a single line when set to `false`. Valid values are `true` or `false`. |
| `skipNullOn` | `String` | `null` | Skips `null` values in the specified data structure. By default, DataWeave does not skip the values. · `arrays` + Ignore and omit `null` values inside arrays from the JSON output, for example, with `output application/json skipNullOn="arrays"`. · `objects` + Ignore key-value pairs that have `null` as the value, for example, with `output application/json skipNullOn="objects"`. · `everywhere` + Apply `skipNullOn` to arrays and objects, for example, `output application/json skipNullOn="everywhere"`. Valid values are `arrays` or `objects` or `everywhere`. |
| `writeAttributes` | `Boolean` | `false` | Converts attributes of a key into child key-value pairs of that key. The attribute key name starts with @. Valid values are `true` or `false`. |

### Supported MIME Types

This format supports the following MIME types.

| MIME Type |
|---|
| `*/json` |
| `**/**+json` |

---

## XML Format

MIME type: `application/xml`

ID: `xml`

The XML data structure is mapped to DataWeave objects that can contain other
objects, strings, or `null` values. XML uses unbounded elements to represent collections, which are mapped to repeated keys in DataWeave objects. In addition, DataWeave natively supports `namespaces`, `CData` an `xsi:types`.

The DataWeave reader for XML input supports the following parsing strategies:

- Indexed
- In-Memory
- Streaming

To understand the parsing strategies that DataWeave readers and writers can apply to this format, see DataWeave Parsing Strategies.

### `CData` Custom Type

`CData` is a custom DataWeave data type for XML that is used to identify a character data (CDATA) block. The `CData` type makes the XML writer wrap content inside a `CDATA` block or to check for an input string inside a `CDATA` block. In DataWeave, `CData` inherits from the type `String`.

### `DocType` Custom Type

`DocType` is a custom DataWeave data type for XML that is used to identify a doctype declaration (DTD).

### Read and Write DTDs

_Introduced in DataWeave 2.5.0. Supported by Mule 4.5.0 and later._

DataWeave can read and write doctype declarations in XML files.

During the reading phase, DataWeave parses the doctype declarations and stores the content as metadata of the root element. The `DocType` value is stored in the `docType` variable. You can use the metadata selector (`^`) to extract the value of that variable with an expression like this one:

- `payload.^docType`
See examples example12, example13, and example14.

> **Note:** :

DTDs are disabled by default even if their declarations are read or written. For details, see XML reader property `supportDtd` in reader properties.

### Examples

The following examples show uses of the XML format.

- example1
- example2
- example3
- example4
- example5
- example6
- example7
- example8
- example9
- example10
- example11
- example12
- example13
- example14

Refer to DataWeave Formats for more detail on available reader and writer properties for various data formats.

#### Example: Stream Input XML Data

This example shows how to set up XML streaming, which requires you to specify the following reader properties:

- `streaming=true`
- `collectionPath="root.repeated"`

The `collectionPath` setting selects the elements to stream.

When streaming, the XML parser can start processing content without having all the XML content.

##### Input

The following XML serves as the input payload to the DataWeave source. Assume that it is the content of an XML file `myXML.xml`.

**myXML.xml**

```xml
<root>
    <text>
        Text
    </text>
    <repeated>
        <user>
            <name>Mariano</name>
            <lastName>de Achaval</lastName>
            <age>36</age>
        </user>
        <user>
            <lastName>Shokida</lastName>
            <name>Leandro</name>
            <age>30</age>
        </user>
        <user>
            <age>29</age>
            <name>Ana</name>
            <lastName>Felissati</lastName>

        </user>
        <user>
            <age>29</age>
            <lastName>Chibana</lastName>
            <name>Christian</name>
        </user>

    </repeated>
</root>
```

##### Source

The reader property settings in the DataWeave script tell the XML reader to stream the input and process the repeated keys. The script uses the DataWeave `map` function to iterate over the repeated keys.

```dataweave
%dw 2.0
var myInput  readUrl('classpath://myXML.xml', 'application/xml', {streaming:true, collectionPath: "root.repeated"})
output application/dw
---
myInput.root.repeated.*user map {
    n: $.name,
    l: $.lastName,
    a: $.age
}
```

##### Output

The script transforms the mapped input XML to the DataWeave (dw) format and MIME type.

```json
[
  {
    "n": "Mariano",
    "l": "de Achaval",
    "a": "36"
  },
  {
    "n": "Leandro",
    "l": "Shokida",
    "a": "30"
  },
  {
    "n": "Ana",
    "l": "Felissati",
    "a": "29"
  },
  {
    "n": "Christian",
    "l": "Chibana",
    "a": "29"
  }
]
```

#### Example: Null or Empty String in XML

Because there is no standard way to represent a `null` value in XML, the reader maps the value to `null` when the `nil` attribute is set to `true`.

##### Input

The following XML serves as the input payload to the DataWeave source.
Notice the `nil` setting in `<xsi:nil="true"`/>.

```xml
<book xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <author xsi:nil="true"/>
</book>
```

##### Source

The DataWeave script transforms the input XML to the JSON format and MIME type.

```dataweave
%dw 2.0
output application/json
---
payload
```

##### Output

The output is in the JSON format. Notice that the `nil` value in the input is transformed to `null`.

```json
{
  "book": {
    "author": null
  }
}
```

#### Example: Output `null` Values for Missing XML Values

The XML reader property `nullValueOn` accepts the value `blank` (the default) or `empty`.

This example uses the `nullValueOn` default, so it maps the values of the `title` and `author` elements to `null`.

##### Input

The following XML serves as input to the DataWeave source. Notice that the `title` and `author` elements lack values.

Assume that this input is content within the file, `myInput.xml`.

**myXML.xml content:**

```xml
<book>
    <author></author>
    <title>

</title>
</book>
```

##### Source

The DataWeave script transforms the XML input to JSON. Note that it
explicitly sets the `nullValueOn` default, `blank`, for demonstration purposes.

```dataweave
%dw 2.0
var myInput readUrl('classpath://myXML.xml', 'application/xml', {nullValueOn: "blank"})
output application/json
---
myInput
```

##### Output

The `title` and `author` keys in the JSON output are assigned `null` values.

```json
{
  "book": {
    "author": null,
    "title": null
  }
}
```

#### Example: Output `null` Values for Missing XML Values

The XML reader property `nullValueOn` accepts the value `blank` (the default) or `empty`.

The example maps the value of the `title` element to a `String` and value of the `author` element to `null` because the XML reader property `nullValueOn` is set to `empty`.

##### Input

The following XML serves as input to the DataWeave source. Notice that the `title` and `author` elements lack values. The difference between the two elements is the space between the starting and ending tags. The tags of the `title` element are separated by line breaks (the hidden characters, `\n`), while the tags of the `author` element are not separated by any characters.

Assume that this input is content within the file, `myInput.xml`.

**myXML.xml content:**

```xml
<book>
    <author></author>
    <title>

</title>
</book>
```

##### Source

The DataWeave script uses a DataWeave variable to input the content of `myXML.xml` and applies the `nullValueOn: "empty"` to it. The script transforms the XML input to JSON.

```dataweave
%dw 2.0
var myInput readUrl('classpath://myXML.xml', 'application/xml', {nullValueOn: "empty"})
output application/json
---
myInput
```

##### Output

The JSON output maps the value of the `author` element to `null` and value of the `title` element to the `String` value `"\n\n"`, which is for the new line characters.

```json
{
  "book": {
    "author": null,
    "title": "\n\n"
  }
}
```

#### Example: Represent XML Attributes in the DataWeave (dw) Format

This example maps XML attributes to a canonical DataWeave representation,
the `application/dw` format and MIME type.

##### Input

The XML serves as the input payload to the DataWeave source. Notice that the input contains XML attributes.

```xml
<users>
  <company>MuleSoft</company>
  <user name="Leandro" lastName="Shokida"/>
  <user name="Mariano" lastName="Achaval"/>
</users>
```

##### Source

The DataWeave script transforms the XML input payload to the DataWeave (dw) format and MIME type.

```dataweave
%dw 2.0
output application/dw
---
payload
```

##### Output

The output shows how the DataWeave (dw) format represents the XML input. Notice how the attributes from the XML input and the empty values are represented.

```dataweave
{
  users: {
    company: "MuleSoft",
    user @(name: "Leandro",lastName: "Shokida"): "",
    user @(name: "Mariano",lastName: "Achaval"): ""
  }
}
```

#### Example: Represent XML Namespaces in the DataWeave (dw) Format

This example maps XML namespaces to a canonical DataWeave representation,
the `application/dw` format and MIME type.

##### Input

The XML serves as the input payload to the DataWeave source. Notice that the input contains XML namespaces.

```xml
<root>
    <h:table xmlns:h="http://www.w3.org/TR/html4/">
      <h:tr>
        <h:td>Apples</h:td>
        <h:td>Bananas</h:td>
      </h:tr>
    </h:table>

    <f:table xmlns:f="https://www.w3schools.com/furniture">
      <f:name>African Coffee Table</f:name>
      <f:width>80</f:width>
      <f:length>120</f:length>
    </f:table>
</root>
```

##### Source

The DataWeave script transforms the XML input payload to the DataWeave (dw) format and MIME type.

```dataweave
%dw 2.0
output application/dw
---
payload
```

##### Output

The output shows how the DataWeave (dw) format represents the XML input. Notice how the namespaces from the XML are represented.

```dataweave
ns h http://www.w3.org/TR/html4/
ns f https://www.w3schools.com/furniture
---
{
  root: {
      h#table: {
        h#tr: {
          h#td: "Apples",
          h#td: "Bananas"
        }
      },
      f#table: {
        f#name: "African Coffee Table",
        f#width: "80",
        f#length: "120"
      }
  }
}
```

#### Example: Create a CDATA Element

This example shows how to use the `CData` type to create a CDATA element in the XML output.

##### Source

The body of the DataWeave script coerces the `String` value to the `CData` type.

```dataweave
%dw 2.0
output application/xml
---
{
    test: "A text <a>" as CData
}
```

##### Output

The output encloses the input `String` value in a CDATA block, which contains the special characters, `<` and `>`, from the input.

```xml
<?xml version='1.0' encoding='UTF-8'?>
<test><![CDATA[A text <a>]]></test>
```

#### Example: Check for CDATA in a `String`

This example indicates whether a given `String` value is CDATA.

##### Input

The XML serves as the input payload to the DataWeave source. Notice that the
`test` element contains a CDATA block.

```xml
<?xml version='1.0' encoding='UTF-8'?>
<test><![CDATA[A text <a>]]></test>
```

##### Source

The DataWeave script uses the `is CData` expression to determine whether the `String` value is CDATA.

```dataweave
%dw 2.0
output application/json
---
{
    test: payload.test is CDATA
}
```

##### Output

The JSON output contains the value `true`, which indicates tha the input `String` value is CDATA.

```json
{
    "test": true
}
```

#### Example: Use the `inlineCloseOn` Writer Property

This example uses the `inlineCloseOn` writer property with the value `none` to act on the key-value pairs from the input.

##### Source

The DataWeave script transforms the body content to XML. Notice that values of the `emptyElement` keys are `null`.

```dataweave
%dw 2.0
output application/xml inlineCloseOn="none"
---
{
  someXml: {
    parentElement: {
      emptyElement1: null,
      emptyElement2: null,
      emptyElement3: null
    }
  }
}
```

##### Output

The `emptyElement` elements are empty. They do not contain the value `null`.

```xml
<?xml version='1.0' encoding='UTF-8'?>
<someXml>
  <parentElement>
    <emptyElement1></emptyElement1>
    <emptyElement2></emptyElement2>
    <emptyElement3></emptyElement3>
  </parentElement>
</someXml>
```

#### Example: Transforms Repeated JSON Keys to Repeated XML Elements

XML encodes collections using repeated (unbounded) elements. DataWeave represents unbounded elements by repeating the same key.

This example shows how to convert the repeated keys in a JSON array of objects into repeated XML elements.

##### Input

The JSON input serves as the payload to the DataWeave source. Notice that the
`name` keys in the array are repeated.

```json
{
  "friends": [
    {"name": "Mariano"},
    {"name": "Shoki"},
    {"name": "Tomo"},
    {"name": "Ana"}
  ]
}
```

##### Source

The DataWeave script selects the value of the `friends` key.

```dataweave
%dw 2.0
output application/xml
---
friends: {
    (payload.friends)
}
```

##### Output

The output represents the `name` keys as XML elements.

```xml
<?xml version='1.0' encoding='UTF-8'?>
<friends>
  <name>Mariano</name>
  <name>Shoki</name>
  <name>Tomo</name>
  <name>Ana</name>
</friends>
```

See also, Example: Outputting Self-closing XML Tags.

#### Example: Transform XML Elements to JSON and Replace Characters

This example iterates over an XML file that contains details of employees, such as the `Id`, `Name`, and `Address`, and converts the file into JSON format. The DataWeave script uses the `replace` function to iterate over each `Address` element and replace the characters `-` and `/` with blank space.

##### Input

The XML input serves as the payload to the DataWeave source. Notice that the `Address` element contains `-` and `/` characters.

```xml
<?xml version='1.0' encoding='UTF-8'?>
<root>
  <employees>
    <Id>1</Id>
    <Name>Mule</Name>
    <Address>MuleSoft Avenue - 123</Address>
  </employees>
  <employees>
    <Id>2</Id>
    <Name>Max</Name>
    <Address>MuleSoft Avenue-456/5/e</Address>
  </employees>
</root>
```

##### Source

The following DataWeave script iterates over the payload elements and performs a mapping to an object. The instruction `payload01.Address replace /([\-\,\/])/ with " "` replaces the `-` and `/` characters with blank spaces.

```dataweave
%dw 2.0
output application/json
---
payload.root.*employees map ((payload01 , indexOfPayload01) ->
  {
     Id: payload01.Id as String,
     Name: payload01.Name as String,
     Address: payload01.Address replace /([\-\,\/])/ with " "
  }
)
```

##### Output

The output represents the transformed XML elements into JSON.

```json
[
  {
    "Id": "1",
    "Name": "Mule",
    "Address": "MuleSoft Avenue   123"
  },
  {
    "Id": "2",
    "Name": "Max",
    "Address": "MuleSoft Avenue 456 5 e"
  }
]
```

#### Example: Read DTD value

The following DataWeave script transforms the XML input payload that contains a `DocType` value into JSON. Notice that extracts the value of that doctype directive using the expression `payload.^docType`.

##### Input

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE cXML SYSTEM "http://xml.cxml.org/schemas/cXML/1.2.014/cXML.dtd">
<cXML xml:lang="en-US" payloadID="1615232861.000506@prd327utl1.int.coupahost.com" timestamp="2021-03-08T11:47:42-08:00">
    <Header>
        <From>
            <Credential domain="NetworkID">
                <Identity>TestIdentity</Identity>
            </Credential>
        </From>
        <To>
            <Credential domain="TEST">
                <Identity>Identity</Identity>
            </Credential>
        </To>
    </Header>
</cXML>
```

##### Source

```dataweave
%dw 2.0
output application/json
---
{
    header: {
        senderId: payload.cXML.Header.From.Credential.Identity,
        receiverId: payload.cXML.Header.To.Credential.Identity,
        docType: payload.^docType
    }
}
```

##### Output

```json
{
  "header": {
    "senderId": "Identity",
    "receiverId": "TestIdentity",
    "docType": {
      "rootName": "cXML",
      "systemId": "http://xml.cxml.org/schemas/cXML/1.2.014/cXML.dtd"
    }
  }
}
```

#### Example: Write a DTD Value

This example shows how to use the `docType` metadata to create a `DocType` value in the XML output.

##### Source

```dataweave
%dw 2.0
output application/xml
ns xml http://www.w3.org/XML/1998/namespace

var cXmlObj = {
  cXML @(payloadID: "9949494", xml#lang: "en-US", timestamp: "2002-02-04T18:39:09-08:00"): {
      Header: {
        From: {
          Credential @(domain: "NetworkId"): {
            Identity: "Identity"
          }
        }
    }
  }
} as Object {
    docType: { rootName: "cXML", systemId: "http://xml.cXML.org/schemas/cXML/1.2.014/cXML.dtd" }
}
---
cXmlObj
```

##### Output

```xml
<?xml version='1.0' encoding='UTF-8'?>
<!DOCTYPE cXML SYSTEM "http://xml.cXML.org/schemas/cXML/1.2.014/cXML.dtd">
<cXML payloadID="9949494" xml:lang="en-US" timestamp="2002-02-04T18:39:09-08:00">
  <Header>
    <From>
      <Credential domain="NetworkId">
        <Identity>Identity</Identity>
      </Credential>
    </From>
  </Header>
</cXML>
```

#### Example: Transform DTD Value to a String Representation

This example uses Dtd Module (dw::xml::Dtd) to transform
a `DocType` value that includes a `systemId` to a string representation.

##### Input

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE cXML SYSTEM "http://xml.cxml.org/schemas/cXML/1.2.014/cXML.dtd">
<cXML xml:lang="en-US" payloadID="1615232861.000506@prd327utl1.int.coupahost.com" timestamp="2021-03-08T11:47:42-08:00">
    <Header>
        <From>
            <Credential domain="NetworkID">
                <Identity>Identity</Identity>
            </Credential>
        </From>
        <To>
            <Credential domain="TEST">
                <Identity>Identity</Identity>
            </Credential>
        </To>
    </Header>
</cXML>
```

##### Source

```dataweave
%dw 2.0
output application/json
import * from dw::xml::Dtd
---
docTypeAsString(payload.^docType)
```

##### Output

```json
"cXML SYSTEM http://xml.cxml.org/schemas/cXML/1.2.014/cXML.dtd"
```

### Configuration Properties

DataWeave supports the following configuration properties for this format.

#### Reader Properties

This format accepts properties that provide instructions for reading input data.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `collectionPath` | `String` | `null` | Sets the path to the location in the document where the collection is located. Accepts a path expression that identifies the location of the elements to stream. |
| `externalEntities` | `Boolean` | `false` | Indicates whether to process external entities. Disabled by default to avoid XML External Entity (XXE) attacks. Valid values are `true` or `false`. |
| `indexedReader` | `Boolean` | `true` | Uses the indexed reader by default when reaching the threshold. Supports US-ASCII, UTF-8 and ISO-8859-1 encodings only. For other encodings, DataWeave uses the in-memory reader. Valid values are `true` or `false`. |
| `maxAttributeSize` | `Number` | `-1` | Sets the maximum number of characters accepted in an XML attribute. _Available since Mule 4.2.1._ |
| `maxEntityCount` | `Number` | `1` | Sets the maximum number of entity expansions. The limit helps avoid Billion Laughs attacks. |
| `nullValueOn` | `String` | `'blank'` | Indicates whether to read an element with empty or blank text as a `null` value. Valid values are `empty` or `none` or `blank`. |
| `optimizeFor` | `String` | `'speed'` | Configures the type of optimization for the XML parser to use. Valid values are `speed` or `memory`. |
| `streaming` | `Boolean` | `false` | Streams input when set to `true`. Use only if entries are accessed sequentially. The input must be a top-level array. See the streaming example, and see DataWeave Readers. Valid values are `true` or `false`. |
| `supportDtd` | `Boolean` | `false` | Enable or disable DTD support. Disabling skips (and does not process) internal and external subsets. You can also enable this property by setting the Mule system property `com.mulesoft.dw.xml.supportDTD`. Note that the default for this property changed from `true` to `false` in Mule version 4.3.0-20210601, which includes the June 2021 patch of DataWeave version 2.3.0. Valid values are `true` or `false`. |

#### Writer Properties

This format accepts properties that provide instructions for writing output data.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `bufferSize` | `Number` | `8192` | Size of the buffer writer, in bytes. The value must be greater than `8`. |
| `defaultNamespace` | `String` | `null` | Specifies the default namespaces of the output XML. |
| `deferred` | `Boolean` | `false` | Generates the output as a data stream when set to `true`, and defers the script's execution until the generated content is consumed. Valid values are `true` or `false`. |
| `doubleQuoteInDeclaration` | `Boolean` | `false` | Escapes double quotes in the XML declaration when set to `true`. Valid values are `true` or `false`. |
| `encoding` | `String` | `null` | The encoding to use for the output, such as UTF-8. |
| `escapeCR` | `Boolean` | `false` | Escapes `CR` characters when set to `true`. Valid values are `true` or `false`. |
| `escapeGT` | `Boolean` | `false` | Escapes '>' characters when set to `true`. Valid values are `true` or `false`. |
| `indent` | `Boolean` | `true` | Write indented output for better readability by default, or compress output into a single line when set to `false`. Valid values are `true` or `false`. |
| `inlineCloseOn` | `String` | `'empty'` | Write an inline close tag, or explicitly open and close tags when the value is `null`. Valid values are `empty` or `none`. |
| `onInvalidChar` | `String` | `null` |  Valid values are `base64` or `ignore` or `none`. |
| `skipNullOn` | `String` | `null` | Skips `null` values in the specified data structure. By default, DataWeave does not skip the values. · `elements` + Ignore and omit `null` elements inside XML output, for example, with `output application/xml skipNullOn="arrays"`. · `attributes ` + Ignore and omit `null` attributes inside XML, for example, with `output application/xml skipNullOn="objects"`. · `everywhere` + Apply `skipNullOn` to elements and attributes, for example, `output application/xml skipNullOn="everywhere"`. Valid values are `elements` or `attributes` or `everywhere`. |
| `writeDeclaration` | `Boolean` | `true` | Writes the XML header declaration when set to `true`. Valid values are `true` or `false`. |
| `writeDeclaredNamespaces` | `String` | `null` | Marks the namespaces to declare in the root element of the XML: · `All`: Write all declared namespaces in the root element. · `ids:<comma separated namespace id>`: Write only the specified namespaces. · `regex:<regex>`: Write only the matching namespaces. |
| `writeNilOnNull` | `Boolean` | `false` | Writes the `nil` attribute for a `null` value when this property is set to `true`. Valid values are `true` or `false`. |

### Supported MIME Types

This format supports the following MIME types.

| MIME Type |
|---|
| `*/xml` |
| `**/**+xml` |

---

## CSV Format

MIME type: `application/csv`

ID: `csv`

The CSV data format is represented as a DataWeave array of objects in which each object represents a row. All simple values are represented as strings.

The DataWeave reader for CSV input supports the following parsing strategies:

- Indexed
- In-Memory
- Streaming

By default, the CSV reader stores input data from an entire file in-memory if the file is 1.5MB or less. If the file is larger than 1.5 MB, the process writes the data to disk. For very large files, you can improve the performance of the reader by setting a streaming property to true.

For additional details, see DataWeave Readers.

### Examples

The following examples show uses of the CSV format.

- example1
- example2

#### Example: Represent CSV Data

The following example shows how DataWeave represents CSV data.

##### Input

The following sample data serves as input for the DataWeave source.

```text
name,lastname,age,gender
Mariano,de Achaval,37,male
Paula,de Estrada,37,female
```

##### Source

The DataWeave script transforms the CSV input payload to the DataWeave (dw) format and MIME type.

```dataweave
%dw 2.0
output application/dw
---
payload
```

##### Output

The DataWeave script produces the following output.

```dataweave
[
  {
    name: "Mariano",
    lastname: "de Achaval",
    age: "37",
    gender: "male"
  },
  {
    name: "Paula",
    lastname: "de Estrada",
    age: "37",
    gender: "female"
  }
]
```

#### Example: Stream CSV Data

By default, the CSV reader stores input data from an entire file in-memory
if the file is 1.5MB or less. If the file is larger than 1.5 MB, the process
writes the data to disk. For very large files, you can improve the performance
of the reader by setting a `streaming` property to `true`. To demonstrate the use of this property, the next example streams a CSV file and transforms it to JSON.

##### Input

The structure of the CSV input looks something like the following. Note that a streamed file is typically much longer.

**CSV File Input for Streaming Example (truncated):**

```text
street,city,zip,state,beds,baths,sale_date
3526 HIGH ST,SACRAMENTO,95838,CA,2,1,Wed May 21 00:00:00 EDT 2018
51 OMAHA CT,SACRAMENTO,95823,CA,3,1,Wed May 21 00:00:00 EDT 2018
2796 BRANCH ST,SACRAMENTO,95815,CA,2,1,Wed May 21 00:00:00 EDT 2018
2805 JANETTE WAY,SACRAMENTO,95815,CA,2,1,Wed May 21 00:00:00 EDT 2018
6001 MCMAHON DR,SACRAMENTO,95824,CA,2,1,,Wed May 21 00:00:00 EDT 2018
5828 PEPPERMILL CT,SACRAMENTO,95841,CA,3,1,Wed May 21 00:00:00 EDT 2018
```

##### XML Configuration

To demonstrate a use of the `streaming` property, the following Mule flow streams a CSV file and transforms it to JSON.

```xml
<flow name="dw-streamingFlow" >
  <scheduler doc:name="Scheduler" >
    <scheduling-strategy >
      <fixed-frequency frequency="1" timeUnit="MINUTES"/>
    </scheduling-strategy>
  </scheduler>
  <file:read
     path="${app.home}/input.csv"
     config-ref="File_Config"
     outputMimeType="application/csv; streaming=true; header=true"/>
  <ee:transform doc:name="Transform Message" >
    <ee:message >
      <ee:set-payload ><![CDATA[%dw 2.0
output application/json
---
payload map ((row) -> {
zipcode: row.zip
})]]></ee:set-payload>
    </ee:message>
  </ee:transform>
  <file:write doc:name="Write"
    config-ref="File_Config1"
    path="/path/to/output/file/output.json"/>
  <logger level="INFO" doc:name="Logger" message="#[payload]"/>
</flow>
```

- The example configures the Read operation (`<file:read/>`) to stream the CSV input by setting `outputMimeType="application/csv; streaming=true"`. The input CSV file is located in the project directory, `src/main/resources`, which is the location of `${app.home}`.
- The DataWeave script in the **Transform Message** component uses the `map`
function to iterate over each row in the CSV payload and select the value
of each field in the `zip` column.
- The Write operation returns a file, `output.json`, which contains the result
of the transformation.
- The Logger prints the same output payload that you see in `output.json`.

##### Output

The CSV streaming example produces the following output.

```json
[
  {
    "zipcode": "95838"
  },
  {
    "zipcode": "95823"
  },
  {
    "zipcode": "95815"
  },
  {
    "zipcode": "95815"
  },
  {
    "zipcode": "95824"
  },
  {
    "zipcode": "95841"
  }
]
```

### Configuration Properties

DataWeave supports the following configuration properties for this format.

#### Reader Properties

This format accepts properties that provide instructions for reading input data.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `bodyStartLineNumber` | `Number` | `0` | Line number on which the body starts. |
| `escape` | `String` | `\` | Character to use for escaping special characters, such as separators or quotes. |
| `header` | `Boolean` | `true` | Indicates whether a CSV header is present. · If `header=true`, you can access the fields within the input by name, for example, `payload.userName`. · If `header=false`, you must access the fields by index, referencing the entry first and the field next, for example, `payload[107][2]`. Valid values are `true` or `false`. |
| `headerLineNumber` | `Number` | `0` | Line number on which the CSV header is located. |
| `ignoreEmptyLine` | `Boolean` | `true` | Indicates whether to ignore an empty line. Valid values are `true` or `false`. |
| `quote` | `String` | `"` | Character to use for quotes. |
| `separator` | `String` | `,` | Character that separates one field from another field. |
| `streaming` | `Boolean` | `false` | Streams input when set to `true`. Use only if entries are accessed sequentially. The input must be a top-level array. See the streaming example, and see DataWeave Readers. Valid values are `true` or `false`. |

#### Writer Properties

This format accepts properties that provide instructions for writing output data.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `bodyStartLineNumber` | `Number` | `0` | Line number on which the body starts. |
| `bufferSize` | `Number` | `8192` | Size of the buffer writer, in bytes. The value must be greater than `8`. |
| `deferred` | `Boolean` | `false` | Generates the output as a data stream when set to `true`, and defers the script's execution until the generated content is consumed. Valid values are `true` or `false`. |
| `encoding` | `String` | `null` | The encoding to use for the output, such as UTF-8. |
| `escape` | `String` | `\` | Character to use for escaping special characters, such as separators or quotes. |
| `header` | `Boolean` | `true` | Indicates whether a CSV header is present. · If `header=true`, you can access the fields within the input by name, for example, `payload.userName`. · If `header=false`, you must access the fields by index, referencing the entry first and the field next, for example, `payload[107][2]`. Valid values are `true` or `false`. |
| `headerLineNumber` | `Number` | `0` | Line number on which the CSV header is located. |
| `ignoreEmptyLine` | `Boolean` | `true` | Indicates whether to ignore an empty line. Valid values are `true` or `false`. |
| `lineSeparator` | `String` | `New Line` | Line separator to use when writing CSV, for example, `"\r\n"`. By default, DataWeave uses the system line separator. |
| `quote` | `String` | `"` | Character to use for quotes. |
| `quoteHeader` | `Boolean` | `false` | Quotes header values when set to `true`. Valid values are `true` or `false`. |
| `quoteValues` | `Boolean` | `false` | Quotes every value when set to `true`, including values that contain special characters. Valid values are `true` or `false`. |
| `separator` | `String` | `,` | Character that separates one field from another field. |

### Supported MIME Types

This format supports the following MIME types.

| MIME Type |
|---|
| `*/csv` |

---

## Flat File Format

MIME type: `application/flatfile`

ID: `flatfile`

The Flat File format supports multiple types of fixed width records within a single message. The schema structure allows you to define how different record types are distinguished, and how the records are logically grouped.

> **Note:** Flat File in DataWeave supports files of up to 15 MB, and the memory requirement is roughly 40 to 1. For example, a 1-MB file requires up to 40 MB of memory to process, so it's important to consider this memory requirement in conjunction with your TPS needs for large flat files. This is not an exact figure; the value might vary according to the complexity of the mapping instructions.

### Example: Specify a Flat File Schema

This example shows a DataWeave script that outputs data in the Flat File format.
Notice that it uses the `schemaPath` and `structureIndent` writer properties.

```dataweave
%dw 2.0
output application/flatfile schemaPath="src/main/resources/test-data/QBReqRsp.esl", structureIdent="QBResponse"
---
payload
```

### Configuration Properties

DataWeave supports the following configuration properties for this format.

#### Reader Properties

This format accepts properties that provide instructions for reading input data.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `allowLenientWithBinaryNotEndElement` | `Boolean` | `false` | When the schema contains elements of type Binary or Packed, the `lenient` option does not allow short records, regardless of the last element's format type. When you set this property to `true`, the validation applies only to cases in which the record ends with type Binary or Packed. Valid values are `true` or `false`. |
| `enforceRequires` | `Boolean` | `false` | Produces an error when set to `true` if a required value is missing. Valid values are `true` or `false`. |
| `missingValues` | `String` | `null` | Fill character used to represent missing values. To activate a non-default setting, set the `useMissCharAsDefaultForFill` property to `true`, and use one of the following values to `missingValues`: · `none` (for the reader) or `NONE` (for the writer): Treats all data as values. · `spaces` (for the reader) or `SPACES` (for the writer): Interprets a field consisting of only spaces as a missing value. Default for flat file and fixed-width formats. · `zeroes` (for the reader) or `ZEROES` (for the writer): Interprets numeric fields consisting of only `0` characters _and_ character fields consisting of only spaces as missing values. · `nulls` (for the reader) or `NULLS` (for the writer): Interprets a field consisting only of `0` bytes as a missing value. Default for COBOL copybook schema. Valid values are `none` or `spaces` or `zeroes` or `nulls`. |
| `notTruncateDependingOnSubjectNotPresent` | `Boolean` | `false` | Fills the entire group when the DEPENDING ON subject is not present. Valid values are `true` or `false`. |
| `recordParsing` | `String` | `'strict'` | Specifies the expected type of separation between lines or records: · `strict`: Line break is expected at exact end of each record. `strict` is the default. · `lenient`: Line break is used, but records can be shorter or longer than the schema specifies. Don't use `lenient` if your payload lacks line breaks. The other options to `recordParsing` support records that lack line breaks. · `noTerminator`: Records follow one another with no separation. This option is preferred for fixed-length records that lack a line break. · `singleRecord`: The entire input is a single record. Note that schemas with type `Binary` or `Packed` don't allow for line break detection, so setting `recordParsing` to `lenient` only allows long records to be handled, not short ones. These schemas also currently only work with certain single-byte character encodings (so not with UTF-8 or any multibyte format). Valid values are `strict` or `lenient` or `noTerminator` or `singleRecord`. |
| `retainEmptyStringFieldsOnParsing` | `Boolean` | `false` | Allow parsing behavior to keep missing string value fields with a default value in the output map Valid values are `true` or `false`. |
| `schemaPath` (Required) | `String` | `null` | Path to the schema definition. Specifies the location in your local disk of the schema file that parses your input. |
| `segmentIdent` | `String` | `null` | Segment identifier in the schema for fixed-width or COBOL copybook schemas. Required when parsing a single segment or record definition if the schema includes multiple segment definitions. |
| `structureIdent` | `String` | `null` | Structure identifier in the schema for flat file schemas. Required when parsing a structure definition if the schema includes multiple structure definitions. |
| `substituteCharacterAsMissingValue` | `Boolean` | `false` | If set to `true` and the `missingValues` property is set to `none`, with `useMissCharAsDefaultForFill` set to `true`, the flat file parser handles the `0x1A` (SUB) character as the missing value. + Otherwise, the flat file parser doesn't handle the `0x1A` character as the missing value. Valid values are `true` or `false`. |
| `truncateDependingOn` | `Boolean` | `false` | For COBOL copybook, truncates DEPENDING ON values to the length used. Valid values are `true` or `false`. |
| `useMissCharAsDefaultForFill` | `Boolean` | `false` | By default, the flat file reader and writer use spaces for missing characters and ignore the setting of the `missingValues` property. When you set this property to `true`, DataWeave honors the `missingValues property` setting. Introduced in DataWeave 2.3 (2.3.0-20210823) for the September 2021 release of Mule 4.3.0-20210823. Valid values are `true` or `false`. |
| `zonedDecimalStrict` | `Boolean` | `false` | For COBOL copybook, uses the 'strict' ASCII form of sign encoding for zoned decimal values. Valid values are `true` or `false`. |

#### Writer Properties

This format accepts properties that provide instructions for writing output data.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `bufferSize` | `Number` | `8192` | Size of the buffer writer, in bytes. The value must be greater than `8`. |
| `deferred` | `Boolean` | `false` | Generates the output as a data stream when set to `true`, and defers the script's execution until the generated content is consumed. Valid values are `true` or `false`. |
| `encoding` | `String` | `null` | The encoding to use for the output, such as UTF-8. |
| `enforceRequires` | `Boolean` | `false` | Produces an error when set to `true` if a required value is missing. Valid values are `true` or `false`. |
| `fillRedefinesByMaxLength` | `Boolean` | `false` | If set to `true`, the flat file module fills the `Redefines` components that are considered to be missing values up to the maximum number of characters set in the `maxLength` parameter. + If set to `false`, the module uses all the defined view options to determine how to fill the `Redefines` components. Valid values are `true` or `false`. |
| `missingValues` | `String` | `null` | Fill character used to represent missing values. To activate a non-default setting, set the `useMissCharAsDefaultForFill` property to `true`, and use one of the following values to `missingValues`: · `none` (for the reader) or `NONE` (for the writer): Treats all data as values. · `spaces` (for the reader) or `SPACES` (for the writer): Interprets a field consisting of only spaces as a missing value. Default for flat file and fixed-width formats. · `zeroes` (for the reader) or `ZEROES` (for the writer): Interprets numeric fields consisting of only `0` characters _and_ character fields consisting of only spaces as missing values. · `nulls` (for the reader) or `NULLS` (for the writer): Interprets a field consisting only of `0` bytes as a missing value. Default for COBOL copybook schema. Valid values are `none` or `spaces` or `zeroes` or `nulls`. |
| `notTruncateDependingOnSubjectNotPresent` | `Boolean` | `false` | Fills the entire group when the DEPENDING ON subject is not present. Valid values are `true` or `false`. |
| `recordTerminator` | `String` | `null` | Line break for a record separator. DataWeave uses this property as a separator only when there are multiple records. Values translate directly to character codes, and `none` leaves no termination on each record. Valid values are `lf` or `cr` or `crlf` or `none`. |
| `schemaPath` (Required) | `String` | `null` | Path to the schema definition. Specifies the location in your local disk of the schema file that parses your input. |
| `segmentIdent` | `String` | `null` | Segment identifier in the schema for fixed-width or COBOL copybook schemas. Required when parsing a single segment or record definition if the schema includes multiple segment definitions. |
| `structureIdent` | `String` | `null` | Structure identifier in the schema for flat file schemas. Required when parsing a structure definition if the schema includes multiple structure definitions. |
| `trimValues` | `Boolean` | `false` | Trim values that are longer than the width of a field. Valid values are `true` or `false`. |
| `truncateDependingOn` | `Boolean` | `false` | For COBOL copybook, truncates DEPENDING ON values to the length used. Valid values are `true` or `false`. |
| `useMissCharAsDefaultForFill` | `Boolean` | `false` | By default, the flat file reader and writer use spaces for missing characters and ignore the setting of the `missingValues` property. When you set this property to `true`, DataWeave honors the `missingValues property` setting. Introduced in DataWeave 2.3 (2.3.0-20210823) for the September 2021 release of Mule 4.3.0-20210823. Valid values are `true` or `false`. |
| `zonedDecimalStrict` | `Boolean` | `false` | For COBOL copybook, uses the 'strict' ASCII form of sign encoding for zoned decimal values. Valid values are `true` or `false`. |

### Supported MIME Types

This format supports this MIME type:

- `*/flatfile`

---

## Fixed Width Format

MIME Type: `application/flatfile`

ID: `flatfile`

Fixed width types are technically considered a type of Flat File format, but
when selecting this option, the Transform component offers you settings that are
better tailored to the needs of this format.

> **Note:** Fixed width in DataWeave supports files of up to 15 MB, and the memory requirement is roughly 40 to 1. For example, a 1-MB file requires up to 40 MB of memory to process, so it's important to consider this memory requirement in conjunction with your TPS needs for large fixed width files. This is not an exact figure; the value might vary according to the complexity of the mapping instructions.

### Supported MIME Types (for Fixed Width)

The Fixed Width format supports the following MIME types.

| MIME Type |
|---|
| `*/flatfile` |

---

## Excel Format

MIME type: `application/xlsx`

ID: `excel`

An Excel workbook is a sequence of sheets. In DataWeave, this is mapped to an
object where each sheet is a key. Only one table is allowed per Excel sheet.
A table is expressed as an array of rows. A row is an object where its keys
are the columns and the values the cell content.

Only `.xlsx` files are supported (Excel 2007). `.xls` files are not supported
by Mule.

The DataWeave reader for Excel input supports the following parsing strategies:

- In-Memory
- Streaming

To understand the parsing strategies that DataWeave readers and writers can apply to this format, see DataWeave Parsing Strategies.

### Excel Type Mapping

The following table shows how Excel types map to DataWeave types.

| Excel Type | DataWeave Type |
|---|---|
| `String` | `String` |
| `Numeric` | `Number` |
| `Boolean` | `Boolean` |
| `Data` | `Date` |

### Examples

The following examples show uses of the Excel format.

- example1
- example2
- example3

#### Example: Represent Excel in the DataWeave (dw) Format

This example shows how DataWeave represents an Excel workbook.

##### Input

The Excel workbook (`Sheet1`) serves as an input payload for the DataWeave source.

**Sheet1:**

```text
.   | A    | B
1   | Id   | Name
2   | 123  | George
3   | 456  | Lucas
```

##### Source

The DataWeave script transforms the Excel input payload to the DataWeave (dw) format and MIME type.

```dataweave
%dw 2.0
output application/dw
---
payload
```

##### Output

The DataWeave output looks like this. You can select values the same way you select values in other objects.

```dataweave
{
    "Sheet1": [
        {
                "A": 123,
                "B": "George"
        },
        {
                "A": 456,
                "B": "Lucas"
        }
    ]
}
```

#### Example: Output an Excel Table

The following DataWeave script outputs an Excel table with the header and fields.

The body of this DataWeave script is a DataWeave object that defines the content of the Excel sheet. The name of the sheet, `Sheet1`, is the key of this object. The value is an array of objects. Each object in the array contains a collection of key-value pairs. The keys in each pair are treated as header values for the
spreadsheet. The values in each pair are treated as data values for a row in the sheet.

The output directive indicates that the output is the Excel format and MIME type. The `header=true` setting indicates that the output includes the header values.

```dataweave
%dw 2.0
output application/xlsx header=true
---
{
  Sheet1: [
    {
      Id: 123,
      Name: George
    },
    {
      Id: 456,
      Name: Lucas
    }
  ]
}
```

For another example, see
Look Up Data in an Excel (XLSX) File.

#### Example: Stream Excel Input

By default, the Excel reader stores input data from an entire file in-memory
if the file is 1.5MB or less. If the file is larger than 1.5 MB, the process
writes the data to disk. For very large files, you can improve the performance
of the reader by setting a `streaming` property to `true`.

The following Configuration XML for a Mule application streams an Excel file and transforms it to JSON.

```xml
<http:listener-config
    name="HTTP_Listener_config"
    doc:name="HTTP Listener config" >
  <http:listener-connection host="0.0.0.0" port="8081" />
</http:listener-config>
<flow name="streaming_flow" >
  <http:listener
    doc:name="Listener"
    config-ref="HTTP_Listener_config"
    path="/"
    outputMimeType="application/xlsx; streaming=true"/>
  <ee:transform doc:name="Transform Message" >
    <ee:message >
      <ee:set-payload ><![CDATA[%dw 2.0
output application/json
---
payload."Sheet Name" map ((row) -> {
    foo: row.a,
    bar: row.b
})]]></ee:set-payload>
    </ee:message>
  </ee:transform>
</flow>
```

The example:

- Configures the HTTP listener to stream the XLSX input
by setting `outputMimeType="application/xlsx; streaming=true"`.
In the Studio UI, you can use the **MIME Type** on the listener to `application/xlsx`
and the **Parameters** for the MIME Type to **Key** `streaming` and **Value** `true`.
- Uses a DataWeave script in the **Transform Message** component to iterate
over each row in the XLSX payload (an XLSX sheet called `"Sheet Name"`) and
select the values of each cell in the row (using `row.a`, `row.b`). It assumes
columns named `a` and `b` and maps the values from each row in those columns
into `foo` and `bar`, respectively.

##### Output

The following image shows the Excel table output.

### Limitations

 * Macros are currently not supported.
 * Charts are ignored.
 * Pivot tables are not supported.
 * Formatting is currently not supported.

### Configuration Properties

DataWeave supports the following configuration properties for this format.

#### Reader Properties

This format accepts properties that provide instructions for reading input data.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `header` | `Boolean` | `true` | Indicates whether the first line of the output contains header field names. Valid values are `true` or `false`. |
| `ignoreEmptyLine` | `Boolean` | `true` | Ignores an empty line by default. Valid values are `true` or `false`. |
| `maxEntrySize` | `Number` | `null` | Sets the maximum number of bytes a single entry in a ZIP file can have. |
| `minInflateRatio` | `Number` | `null` | Sets the ratio between de- and inflated bytes to detect zip bomb. For example, if you set the value to 1 percent (= 0.01d) when the compression is better than 1 percent for any given read package part, the parsing fails to indicate a zip bomb. |
| `streaming` | `Boolean` | `false` | Streams input when set to `true`. Use only if entries are accessed sequentially. The input must be a top-level array. See the streaming example, and see DataWeave Readers. Valid values are `true` or `false`. |
| `tableLimit` | `String` | `'Unbounded'` | Position of the last column in each row. Accepts a pattern `<Column>` (for example, `'A'` or `'AB'`), the value `'HeaderSize'`, which uses the location of the last header, or 'Unbounded', which consumes each row. |
| `tableOffset` | `String` | `null` | Sets the position of the first cell. Accepts the pattern `<Column><Row>`, for example, `A1` or `B3`. |
| `zipBombCheck` | `Boolean` | `true` | Turns off the zip bomb (decompression bomb) check when set to `false`. Valid values are `true` or `false`. |

#### Writer Properties

This format accepts properties that provide instructions for writing output data.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `bufferSize` | `Number` | `8192` | Size of the buffer writer, in bytes. The value must be greater than `8`. |
| `deferred` | `Boolean` | `false` | Generates the output as a data stream when set to `true`, and defers the script's execution until the generated content is consumed. Valid values are `true` or `false`. |
| `header` | `Boolean` | `true` | Indicates whether the first line of the output contains header field names. Valid values are `true` or `false`. |
| `ignoreEmptyLine` | `Boolean` | `true` | Ignores an empty line by default. Valid values are `true` or `false`. |
| `maxEntrySize` | `Number` | `null` | Sets the maximum number of bytes a single entry in a ZIP file can have. |
| `minInflateRatio` | `Number` | `null` | Sets the ratio between de- and inflated bytes to detect zip bomb. For example, if you set the value to 1 percent (= 0.01d) when the compression is better than 1 percent for any given read package part, the parsing fails to indicate a zip bomb. |
| `tableOffset` | `String` | `null` | Sets the position of the first cell. Accepts the pattern `<Column><Row>`, for example, `A1` or `B3`. |
| `zipBombCheck` | `Boolean` | `true` | Turns off the zip bomb (decompression bomb) check when set to `false`. Valid values are `true` or `false`. |

### Supported MIME Types

This format supports the following MIME types.

| MIME Type |
|---|
| `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet` |
| `application/xlsx` |

---

## Java Format

MIME type: `application/java`

ID: `java`

For the Java data format, DataWeave attempts to map any Java value to a DataWeave value, most often by matching the semantics of DataWeave and Java.

### Java Value Mapping

This table maps Java classes to DataWeave types:

| Java Class | DataWeave |
|---|---|
| `java.lang.String` | `String` |
| `Enum` | `String` |
| `Class` | `String` |
| `UUID` | `String` |
| `CharSequence` | `String` |
| `Char` | `String` |
| `java.sql.Clob` | `String` |
| `java.io.Reader` | `String` |
| `int` | `Number` |
| `long` | `Number` |
| `double` | `Number` |
| `short` | `Number` |
| `BigInteger` | `Number` |
| `BigDecimal` | `Number` |
| `AtomicInteger` | `Number` |
| `AtomicLong` | `Number` |
| `boolean` | `Boolean` |
| `AtomicBoolean` | `Boolean` |
| `java.util.Collection` | `Array` |
| `java.lang.Iterable` | `Array` |
| `java.util.Iterator` | `Array` |
| `java.util.Map` | `Object` |
| `java.util.Optional` | `Null` or `Value` |
| `java.util.OptionalInt` | `Null` or `Number` |
| `java.util.OptionalDouble` | `Null` or `Number` |
| `java.util.OptionalLong` | `Null` or `Number` |
| `byte[]` | `Binary` |
| `java.lang.InputStream` | `Binary` |
| `java.nio.ByteBuffer` | `Binary` |
| `byte` | `Binary` |
| `java.lang.File` | `Binary` |
| `java.time.Instant` | `LocalDateTime` |
| `java.time.LocalDateTime` | `LocalDateTime` |
| `java.sql.Timestamp` | `LocalDateTime` |
| `java.sql.Date` | `LocalDateTime` |
| `java.util.Date` | `LocalDateTime` |
| `java.time.ZonedDateTime` | `DateTime` |
| `java.time.LocalTime` | `LocalTime` |
| `java.time.OffsetTime` | `Time` |
| `java.time.LocalDate` | `Date` |
| `java.time.ZoneOffset` | `TimeZone` |
| `java.util.Calendar` | `DateTime` |
| `java.util.XMLGregorianCalendar` | `DateTime` |
| `*[]` | `Array` |

> **Important:** If a Java class isn't present in the table, DataWeave treats it as a `JavaBean` and maps it as an `Object` type. In this case, DataWeave takes all properties from the Java getters.

### Metadata

DataWeave supports the `^class` metadata for the Java format.

All Java objects are associated with a class. DataWeave maintains this association by mapping the class to a Metadata property.

`payload.^class` returns the name of the class of the `payload`.

The Java writer uses the metadata property to discover the Java class to which the DataWeave value maps. That is, DataWeave uses the metadata property to determine which Java class is to be created from a given DataWeave value. For example, the expression `output application/java --- now() as DateTime {class: "java.util.Calendar"}` creates a `java.util.Calendar`.

### Enum Custom Type

The Java format supports the `Enum` custom type. To put a Java `enum` value into a `java.util.Map`, the DataWeave Java module defines a custom type called `Enum`.
This custom type enables you to handle a given string as the name of a specified `enum` type. You must use the `class` metadata property when specifying the Java class name of the enum, for example: `{gender: "Female" as Enum {class: "org.mycompany.Gender"}}`

### Handling `java.io.InputStream` Instances

Using `java.io.InputStream` instances in DataWeave, whether running DataWeave functions, calling Java methods from DataWeave code, or writing them to an output, requires understanding how DataWeave manages `java.io.InputStream` instances.

The Java format makes a deep copy of the `java.io.InputStream` instance. As a result, DataWeave creates a new `java.io.InputStream` instance that can be reused later in your script while retaining the content of the original stream.

However, if the original `java.io.InputStream` doesn't support repeatable streams, it may get consumed and become unusable.

To avoid unexpected behavior, always check whether your `java.io.InputStream` is repeatable before processing it multiple times.

### Examples

The following examples show uses of the Java format.

- example1
- example2
- example3

#### Class Definitions

The Java examples use these class definitions:

- `User`
- `Customer` (which extends `User`)

**User class:**

```java
class User {
    private String name;
    private String lastName;

    public User(){

    }

    public User(String name, String lastName){
        this.name = name;
        this.lastName = lastName;
    }

    public void setName(String name){
        this.name = name;
    }

     public void setLastName(String lastName){
        this.lastName = lastName;
    }

    public String getName(){
        return name;
    }

    public String getLastName(){
        return lastName;
    }
}
```

This class extends `User`.

**Customer class:**

```java
import java.util.Calendar;
class Customer extends User {
    private Calendar expirationDate;
    private User salesRepr;

    public User(){

    }

    public User(String name, String lastName,Calendar expirationDate){
        super(name,lastName);
        this.expirationDate = expirationDate;
    }

    public void setSalesRepr(User salesRepr){
        this.salesRepr = salesRepr;
    }

    public User getSalesRepr(){
        return this.salesRepr;
    }

    public void  setExpirationDate(Calendar expirationDate){
        this.expirationDate = expirationDate;
    }

    public Calendar getExpirationDate(){
        return this.expirationDate;
    }
}
```

#### Example: Access Values of Java Properties

This example shows how to access the values of Java properties.

##### Input

The `User` values serves as the input payload to the DataWeave script.

```text
new User("Leandro", "Shokida")
```

##### Source

The DataWeave scripts transforms the input value to JSON.

```dataweave
output application/json
---
{
    a: payload.name,
    b: payload.lastName
}
```

##### Output

The output is a JSON object that contains key-value pairs. The values are the `name` and `lastName` values from the input `User` object.

```json
{
    "a": "Leandro",
    "b": "Shokida"
}
```

#### Example: Create a Customer Object

This example shows how to create an instance of a `Customer` class. The script outputs the object in the JSON format and MIME type.

Notice that it's not necessary to specify the class of inner properties because their class is inferred from the parent class definition.

```dataweave
output application/json
---
{
    name: "Tomo",
    lastName: "Chibana",
    expirationDate: now(),
    salesRepr: {
        name: "Mariano",
        lastName: "de Achaval",
    }
} as Object {class: "Customer"}
```

#### Example: Use a Generic

This example relies on generic support in the class name to create a `java.util.ArrayList` of `User` objects.

Don't use a generic to specify the class in each instance. The class is taken from the generic in the list.

```dataweave
output application/json
---
[{
    name: "Tomo",
    lastName: "Chibana"
},
{
    name: "Ana",
    lastName: "Felissati"
},
{
    name: "Leandro",
    lastName: "Shokida"
}
] as Array {class: "java.util.ArrayList<User>"}
```

### Java Support

Starting with version 2.6, DataWeave supports Java 17. Java 17 adds restrictions in encapsulation and reflective access that affects the Java Format. Because DataWeave uses Java's reflection API to read and write Java objects, ensure that the objects your application uses are Plain Old Java Objects (POJOs) containing:

- Default constructor
- Getters for all properties
- Setters for all properties

### Examples of Java Support

These examples run using Java 17 and language level 2.6.

- example4
- example5

#### Example: Create a Java Object Instance

This example shows how to create a Java object instance.

##### User Class

The Java example uses this class:

```java
public class User {
   private String name;
   private String lastName;
   public User(){
   }
   public String getName(){
       return name;
   }
   public String getLastName(){
       return lastName;
   }
}
```

##### DataWeave Script

```java
{name: "Tomo", lastName: "Chibana" } as Object {class: "User"}
```

##### Output

The expected output is an instance of the user class. Because the user class definition doesn't have the proper setters, the output is `IllegalAccessException`.

```java
java.lang.IllegalAccessException - class
org.mule.weave.v2.module.pojo.reader.PropertyDefinition (in module org.mule.weave.module.java) cannot access a member of class User with modifiers "private
```

#### Example: Access the Values of Java Properties

This example shows how to access the values of Java properties.

##### Item Class

The Java example uses the following class:

```java
public class Item {
	private String name;
	private int quantity;

	public Item() {
	}
    public Item(String name, int quantity) {
		this.name = name;
		this.quantity = quantity;
	}
	public void setName(String name) {
		this.name = name;
	}
	public void setQuantity(int quantity) {
		this.quantity = quantity;
	}
}
```

##### Input

```text
new Item("Pencil", 5)
```

##### DataWeave Script

```dataweave
output application/json
---
{
    "name": "payload.name",
    "quantity": "payload.quantity"
}
```

##### Output

The expected output is a JSON object.

```json
{
    "name": "Pencil",
    "quantity": "5"
}
```

Because the item class definition doesn't have the proper getters, the output is `IllegalAccessException`.

```java
java.lang.IllegalAccessException: class
org.mule.weave.v2.module.pojo.reader.PropertyDefinition (in module org.mule.weave.module.java) cannot access a member of class Item with modifiers "private"
```

#### Troubleshooting Common Errors

To resolve conflicts, ensure that you:

- Update your class definitions to follow the POJOs structure (recommended).
- Use the compatibility flag `com.mulesoft.dw.java.disable_set_accessible=false` to allow accessible flag modification for reflection objects.
This approach is a workaround and works for customer domain classes only. Note that the usage of this compatibility flag might not affect future versions.

### Configuration Properties

DataWeave supports these configuration properties for this format.

#### Reader Properties

There are no reader properties for this format.

#### Writer Properties

This format accepts properties that provide instructions for writing output data.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `duplicateKeyAsArray` | `Boolean` | `false` | Converts the values of duplicate keys in an object to a single array of values to the duplicated key. Valid values are `true` or `false`. |
| `writeAttributes` | `Boolean` | `false` | Converts attributes of a key into child key-value pairs of that key. The attribute key name starts with @. Valid values are `true` or `false`. |

### Supported MIME Types

This format supports this MIME type:

- `*/java`

---

## YAML Format

MIME type: `application/yaml`

ID: `yaml`

Values in the YAML data format map one-to-one with DataWeave values.
DataWeave natively supports all of the following YAML types:

- `String`
- `Boolean`
- `Number`
- `Nil`
- `Mapping`
- `Sequences`

### Example: Represent YAML in the DataWeave Format (dw)

This example shows how DataWeave represents YAML values.

#### Input

The following YAML snippet serves as the input payload for the DataWeave source
in this example.

```yaml
american:
  - Boston Red Sox
  - Detroit Tigers
  - New York Yankees
national:
  - New York Mets
  - Chicago Cubs
  - Atlanta Braves
```

#### Source

The DataWeave script transforms the YAML encoded input payload to the DataWeave (dw) format and MIME type.

```dataweave
%dw 2.0
output application/dw
---
payload
```

#### Output

The following output shows how the YAML input is represented in the DataWeave (`dw`) format.

```dataweave
{
  "american": [
    "Boston Red Sox",
    "Detroit Tigers",
    "New York Yankees"
  ],
  "national": [
    "New York Mets",
    "Chicago Cubs",
    "Atlanta Braves"
  ]
}
```

### Configuration Properties

DataWeave supports the following configuration properties for this format.

#### Reader Properties

This format accepts properties that provide instructions for reading input data.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `maxEntityCount` | `Number` | `1` | Sets the maximum number of entity expansions. The limit helps avoid Billion Laughs attacks. |

#### Writer Properties

This format accepts properties that provide instructions for writing output data.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `bufferSize` | `Number` | `8192` | Size of the buffer writer, in bytes. The value must be greater than `8`. |
| `deferred` | `Boolean` | `false` | Generates the output as a data stream when set to `true`, and defers the script's execution until the generated content is consumed. Valid values are `true` or `false`. |
| `encoding` | `String` | `'UTF-8'` | The encoding to use for the output, such as UTF-8. |
| `skipNullOn` | `String` | `null` | Skips `null` values in the specified data structure. By default, DataWeave does not skip the values. · `arrays` + Ignore and omit `null` values inside arrays from the YAML output, for example, with `output application/yaml skipNullOn="arrays"`. · `objects` + Ignore key-value pairs that have `null` as the value, for example, with `output application/yaml skipNullOn="objects"`. · `everywhere` + Apply `skipNullOn` to arrays and objects, for example, `output application/yaml skipNullOn="everywhere"`. Valid values are `arrays` or `objects` or `everywhere`. |
| `writeDeclaration` | `Boolean` | `true` | Indicates whether to write the header declaration or not. Valid values are `true` or `false`. |

### Supported MIME Types

This format supports the following MIME types.

| MIME Type |
|---|
| `application/yaml` |
| `text/yaml` |
| `application/x-yaml` |
| `text/x-yaml` |

---

## Text Plain Format

MIME type: `text/plain`

ID: `text`

The Text Plain format represents text as a string.

Note that DataWeave parses, encodes, and stores this format into RAM memory.

### Example

This example shows how DataWeave represents Text Plain data.

#### Input

The Plain Text data serves as the input payload to the DataWeave source.

```text
This is text plain
```

#### Source

The DataWeave script transforms the Text PLain input payload to the DataWeave (dw) format and MIME type. It returns a string.

```dataweave
output application/dw
---
payload
```

#### Output

Because the DataWeave (dw) output is a string, it is wrapped in quotation marks.

```dataweave
"This is text plain"
```

### Configuration Properties

DataWeave supports the following configuration properties for this format.

#### Reader Properties

There are no reader properties for this format.

#### Writer Properties

This format accepts properties that provide instructions for writing output data.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `bufferSize` | `Number` | `8192` | Size of the buffer writer, in bytes. The value must be greater than `8`. |
| `deferred` | `Boolean` | `false` | Generates the output as a data stream when set to `true`, and defers the script's execution until the generated content is consumed. Valid values are `true` or `false`. |
| `encoding` | `String` | `null` | The encoding to use for the output, such as UTF-8. |

### Supported MIME Types

This format supports the following MIME types.

| MIME Type |
|---|
| `text/plain` |

---

## URL Encoded Format

MIME type: `application/x-www-form-urlencoded`

ID: `urlencoded`

URL encoded data represents a collection of key-value pairs. DataWeave represents these values as an object in which each value is a string.

### Examples

The following examples show uses of the URL Encoded format:

- example1
- example2
- example3
- example4

#### Example: Represent URL Encoded Data in the DataWeave (dw) Format

This example shows how DataWeave represents simple URL encoded data.

##### Input

The URL encoded data serves as input payload to the DataWeave source.

```text
name=Mariano&lastName=de+Achaval
```

##### Source

The DataWeave script transforms the URL encoded input payload to the DataWeave (dw) format and MIME type.

```dataweave
%dw 2.0
output application/dw
---
payload
```

##### Output

The output is a DataWeave object that contains a collection of key-value pairs from the input.

```dataweave
{
    "name": "Mariano",
    "lastName": "de Achaval"
}
```

#### Example: Generate URL Encoded Data from a JSON Object

This example shows how to generate URL Encoded data.

##### Input

The JSON object serves as the input payload to the DataWeave source.

```json
{
  "name": "Mariano"
}
```

##### Source

The DataWeave script selects the value of the `name` key in the input payload
and transforms all values of the object in the body of the script to the
`urlencoded` format.

```dataweave
%dw 2.0
output urlencoded
---
{
    name: payload.name,
    age: 37
}
```

##### Output

The output is URL encoded data that is constructed from the key-value pairs
in the body of the DataWeave script.

```text
name=Mariano&age=37
```

#### Example: Generate URL Encoded Data from a Collection of Key-Value Pairs

This DataWeave script produces the URL encoded output.

##### Source

The DataWeave script transforms the format of the JSON input found within the body of the script into the URL Encoded format.

```dataweave
%dw 2.0
output application/x-www-form-urlencoded
---
{
  "key" : "value",
  "key 1": "@here",
  "key" : "other value",
  "key 2%": null
}
```

##### Output

The output shows the input data in the URL Encoded format.

```text
key=value&key+1=%40here&key=other+value&key+2%25
```

#### Example: Transform URL Encoded Data to the Text Plain Format

This example transforms URL Encoded input into the Text Plain format and MIME type.

##### Source

The DataWeave script reads the URL Encoded data and concatenates values of the selected keys.

```dataweave
%dw 2.0
var myData  read('key=value&key+1=%40here&key=other+value&key+2%25', 'application/x-www-form-urlencoded')
output text/plain
---
myData.*key[0] ++ myData.'key 1'
```

##### Output

The output is in Text Plain format.

```text
value@here
```

### Configuration Properties

DataWeave supports the following configuration properties for this format.

#### Reader Properties

There are no reader properties for this format.

#### Writer Properties

This format accepts properties that provide instructions for writing output data.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `bufferSize` | `Number` | `8192` | Size of the buffer writer, in bytes. The value must be greater than `8`. |
| `deferred` | `Boolean` | `false` | Generates the output as a data stream when set to `true`, and defers the script's execution until the generated content is consumed. Valid values are `true` or `false`. |
| `encoding` | `String` | `null` | The encoding to use for the output, such as UTF-8. |

### Supported MIME Types

This format supports the following MIME types.

| MIME Type |
|---|
| `application/x-www-form-urlencoded` |

---

## Newline Delimited JSON (ndjson) Format

MIME type: `application/x-ndjson`

ID: `ndjson`

DataWeave represents the Newline Delimited JSON format (ndjson) as an array of objects. Each line of the ndjson format is mapped to one object in the array.

These parser strategies are supported by the ndjson reader:

- In-memory
- Streaming

For details, see DataWeave Readers.

### Examples

The following examples show uses of the ndjson format.

- example1
- example2

#### Example

This example shows how DataWeave represents a simple ndjson input.

##### Input

```text
{"name": "Leandro","lastName": "Shokida"}
{"name": "Mariano","lastName": "De Achaval"}
```

##### Source

The DataWeave script transforms the ndjson input to the DataWeave (dw) format and MIME type.

```dataweave
%dw 2.0
output application/dw
---
payload
```

##### Output

The DataWeave (dw) format outputs the ndjson input into an array of comma-separated objects.

```text
[
    {"name": "Leandro","lastName": "Shokida"},
    {"name": "Mariano","lastName": "De Achaval"}
]
```

#### Example

This example shows that the ndjson reader ignores all lines of ndjson data that are invalid if `skipInvalid=true`.

##### Input

The input to the DataWeave source includes valid and invalid lines of ndjson data. Assume that the input is from a file `myInput.ndjson`.

**myInput.ndjson:**

```text
{"name": "Christian"
{"name": "Mariano"}
{"name": "Tomo"
{"name": "Shoki"}
```

##### Source

The DataWeave script inputs the contents of the input file `myInput.ndjson`, applies the `skipInvalid=true` reader property, and transforms the input to the JSON format and MIME type.

```dataweave
%dw 2.0
var myInput = readUrl('classpath://myInput.ndjson', 'application/x-ndjson, {skipInvalid=true})
output application/json
---
myInput
```

##### Output

The JSON output is an array of the valid objects from the ndjson input.

```text
[
  {
    "name": "Mariano"
  },
  {
    "name": "Shoki"
  }
]
```

### Configuration Properties

DataWeave supports the following configuration properties for this format.

#### Reader Properties

This format accepts properties that provide instructions for reading input data.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `ignoreEmptyLine` | `Boolean` | `true` | Ignores empty lines. Valid values are `true` or `false`. |
| `skipInvalid` | `Boolean` | `false` | Skips invalid records and ignores values that aren't valid in this format. Valid values are `true` or `false`. |

#### Writer Properties

This format accepts properties that provide instructions for writing output data.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `bufferSize` | `Number` | `8192` | Size of the buffer writer, in bytes. The value must be greater than `8`. |
| `deferred` | `Boolean` | `false` | Generates the output as a data stream when set to `true`, and defers the script's execution until the generated content is consumed. Valid values are `true` or `false`. |
| `encoding` | `String` | `'UTF-8'` | Encoding that the writer uses for output. Defaults to "UTF-8". |
| `skipNullOn` | `String` | `null` | Skips `null` values. By default, DataWeave does not skip. · `arrays` + Ignore and omit `null` values inside arrays from the JSON output, for example, with `output application/x-ndjson skipNullOn="arrays"`. · `objects` + Ignore key-value pairs that have `null` as the value, for example, with `output application/x-ndjson skipNullOn="objects"`. · `everywhere` + Apply `skipNullOn` to arrays and objects, for example, `output application/x-ndjson skipNullOn="everywhere"`. Valid values are `arrays` or `objects` or `everywhere`. |
| `writeAttributes` | `Boolean` | `false` | Converts attributes of a key into child key-value pairs of that key. The attribute key name starts with `@`. Valid values are `true` or `false`. |

### Supported MIME Types

This format supports these MIME types:

- `application/x-ndjson`
- `application/x-ldjson`

---

## Multipart (Form Data) Format

MIME type: `multipart/form-data`

ID: `multipart`

DataWeave supports Multipart subtypes, in particular `form-data`. These formats
enable you to handle several different data parts in a single payload,
regardless of the format each part has. To distinguish the beginning and end of
a part, a boundary is used and metadata for each part can be added through
headers.

DataWeave represents a Multipart document with the given `Object` structure:

```text
type Multipart = {
  preamble?: String,
  parts: {
    _?: MultipartPart
  }
}
type MultipartPart = {
  headers?: {
    "Content-Disposition"?: {
      name: String,
      filename?: String
    },
    "Content-Type"?: String
  },
  content: Any
}
```

### Examples

The following examples show uses of the Multipart format.

- example1
- example2
- example3
- example4
- example5

#### Example: Multipart

This example shows how DataWeave reads simple Multipart content.

##### Input

The Multipart input serves as the payload to the DataWeave source.

```text
--34b21
Content-Disposition: form-data; name="text"
Content-Type: text/plain
Book
--34b21
Content-Disposition: form-data; name="file1"; filename="a.json"
Content-Type: application/json
{
"title": "Java 8 in Action",
"author": "Mario Fusco",
"year": 2014
}
--34b21
Content-Disposition: form-data; name="file2"; filename="a.html"
Content-Type: text/html

<title> Available for download! </title>
--34b21--
```

##### Source

The DataWeave script transforms the Multipart input payload to the DataWeave (dw) format.

```text
%dw 2.0
output application/dw
---
payload
```

##### Output

The output shows how the DataWeave (dw) format represents the Multipart input. Note that the `raw` and `content` values are  shortened for brevity. The full values are longer.

```text
{
    parts: {
        text: {
            headers: {
                "Content-Disposition": {
                    name: "text",
                    subtype: "form-data"
                },
                "Content-Type": "text/plain"
            },
        content: "Book" as String {
            raw: "Qm9vaw==" as Binary {
                    base: "64"
                },
                encoding: null,
                mediaType: "text/plain",
                mimeType: "text/plain"
            }
        },
        file1: {
            headers: {
                "Content-Disposition": {
                    name: "file1",
                    filename: "a.json",
                    subtype: "form-data"
                },
                "Content-Type": "application/json"
            },
            content: {
                title: "Java 8 in Action",
                author: "Mario Fusco",
                year: 2014
            } as Object {
                raw: "ewogICJ0aXRsZSI6ICJKYXZhI...==" as Binary {
                    base: "64"
                },
                encoding: null,
                mediaType: "application/json",
                mimeType: "application/json"
            }
        },
        file2: {
            headers: {
                "Content-Disposition": {
                    name: "file2",
                    filename: "a.html",
                    subtype: "form-data"
                },
                "Content-Type": "text/html"
            },
            content: "PCFET0NUWVBFIGh0bWw+Cjx0aXRsZT4KI...==" as Binary {
                base: "64"
            }
       }
    }
}
```

#### Example: Access and Transform Data from Parts

Within a DataWeave script, you can access and transform data from any of the
parts by selecting the `parts` element. Navigation can be array-based or key-based when parts feature a name to reference them by. The part's data can be
accessed through the `content` keyword, while headers can be accessed through
the `headers` keyword.

##### Input

This example serves as input to separate DataWeave scripts. It shows a raw `multipart/form-data` payload with a `34b21` boundary consisting of 3 parts:

- a `text/plain` one named `text`
- an `application/json` file (`a.json`) named `file1`
- a `text/html` file (`a.html`) named `file2`

**Raw Multipart Data:**

```text
--34b21
Content-Disposition: form-data; name="text"
Content-Type: text/plain

Book
--34b21
Content-Disposition: form-data; name="file1"; filename="a.json"
Content-Type: application/json

{
  "title": "Java 8 in Action",
  "author": "Mario Fusco",
  "year": 2014
}
--34b21
Content-Disposition: form-data; name="file2"; filename="a.html"
Content-Type: text/html

<!DOCTYPE html>
<title>
  Available for download!
</title>
--34b21--
```

##### Source

The following DataWeave script uses the raw `multipart/form-data` payload as input to produce `Book:a.json`.

**Reading Multipart Content:**

```dataweave
%dw 2.0
output text/plain
---
payload.parts.text.content ++ ':' ++ payload.parts[1].headers.'Content-Disposition'.filename
```

#### Example: Generate Multipart Content

You can generate multipart content that DataWeave uses to build an object with a
list of parts, each containing its headers and content. The following
DataWeave script produces the raw multipart data (previously analyzed)
if the HTML data is available in the payload.

> **Note:** To provide a consistent output in the DataWeave documentation, the example hardcodes the `boundary` property.

However, you do not need to hardcode this property in most cases because DataWeave generates a random boundary and adds it to the
output MIME type.

**Writing Multipart Content:**

```dataweave
%dw 2.0
output multipart/form-data boundary='34b21'
---
{
  parts : {
    text : {
      headers : {
        "Content-Type": "text/plain"
      },
      content : "Book"
    },
    file1 : {
      headers : {
        "Content-Disposition" : {
            "name": "file1",
            "filename": "a.json"
        },
        "Content-Type" : "application/json"
      },
      content : {
        title: "Java 8 in Action",
        author: "Mario Fusco",
        year: 2014
      }
    },
    file2 : {
      headers : {
        "Content-Disposition" : {
            "filename": "a.html"
        },
        "Content-Type" : payload.^mimeType
      },
      content : payload
    }
  }
}
```

Notice that the key determines the part's name if the name is not explicitly
provided in the `Content-Disposition` header, and note that DataWeave can
handle content from supported formats, as well as references to unsupported
ones, such as HTML.

The following example shows how to send the current payload as a file part in a multipart form-data. You need to use a DataWeave script similar to the following:

```dataweave
%dw 2.0
input payload application/xml
output multipart/form-data boundary="----myboundary----"
---
{
  parts: {
    filePart: {
      headers: {
        "Content-Disposition": {
          "name": "<NAME>",
          "filename": "<FILE_NAME>.<FILE_EXTENSION>"
        },
        "Content-Type": "<FILE_CONTENT-TYPE>"
      },
      content: payload
    },
    otherJsonPart: {
      content: '{"name": "sampleFile.xml", "sampleFile": {"type": "sample"} }'
    }
  }
}
```

- `boundary` sets the boundary value, for example `"----myboundary----"`.
- `<NAME>` is the tag name of your file, for example `"sampleFile"`.
- `<FILE_NAME>.<FILE_EXTENSION>` is the filename to populate the payload content, for example `"sampleFile.xml"`.
- `<FILE_CONTENT-TYPE>` matches the content of the file you send, for example `"application/xml"`.
- The content of the file is the current payload.

This example contains two parts in the multipart which are the file and the `otherJsonPart`. In case you want to add more parts, add them under the `parts:{}` section with the following format:

```dataweave
  <PART_NAME>: {
    content: <PART_CONTENT>
  }
```

- `<PART_NAME>` is the name of the part without quotes, for example `json`.
- `<PART_CONTENT>` is the content for that part, for example `'{"name": "sampleFile.xml", "sampleFile": {"type": "sample"} }'`.

Based on the following XML input:

```xml
<Customers>
	<Customer>
		<Number>1</Number>
		<FirstName>Fred</FirstName>
		<LastName>Landis</LastName>
		<Address>
			<Street>Oakstreet</Street>
			<City>Boston</City>
			<ZIP>23320</ZIP>
			<State>MA</State>
		</Address>
	</Customer>
	<Customer>
		<Number>2</Number>
		<FirstName>Michelle</FirstName>
		<LastName>Butler</LastName>
		<Address>
			<Street>First Avenue</Street>
			<City>San-Francisco</City>
			<ZIP>44324</ZIP>
			<State>CA</State>
		</Address>
	</Customer>
	<Customer>
		<Number>3</Number>
		<FirstName>Ted</FirstName>
		<LastName>Little</LastName>
		<Address>
			<Street>Long Way</Street>
			<City>Los-Angeles</City>
			<ZIP>34424</ZIP>
			<State>CA</State>
		</Address>
	</Customer>
</Customers>
```

The DataWeave script is:

```dataweave
%dw 2.0
output multipart/form-data  boundary="----myboundary----"
---
{
  parts: {
    filePart: {
      headers: {
        "Content-Disposition": {
          "name": "test",
          "filename": "sampleFile.xml"
        },
        "Content-Type": "application/xml"
      },
      content: payload
    },
    otherJsonPart: {
      content: '{"name": "sampleFile.xml", "sampleFile": {"type": "sample"} }'
    }
  }
}
```

The output multipart is:

Content-Type: application/xml
Content-Disposition: form-data; name="test"; filename="sampleFile.xml"

<Customers>
  <Customer>
    <Number>1</Number>
    <FirstName>Fred</FirstName>
    <LastName>Landis</LastName>
    <Address>
      <Street>Oakstreet</Street>
      <City>Boston</City>
      <ZIP>23320</ZIP>
      <State>MA</State>
    </Address>
  </Customer>
  <Customer>
    <Number>2</Number>
    <FirstName>Michelle</FirstName>
    <LastName>Butler</LastName>
    <Address>
      <Street>First Avenue</Street>
      <City>San-Francisco</City>
      <ZIP>44324</ZIP>
      <State>CA</State>
    </Address>
  </Customer>
  <Customer>
    <Number>3</Number>
    <FirstName>Ted</FirstName>
    <LastName>Little</LastName>
    <Address>
      <Street>Long Way</Street>
      <City>Los-Angeles</City>
      <ZIP>34424</ZIP>
      <State>CA</State>
    </Address>
  </Customer>
</Customers>
```text
Content-Disposition: form-data; name="otherJsonPart"

{"name": "sampleFile.xml", "sampleFile": {"type": "sample"} }
```

```text

[[example4]]
=== Example: Iterate through Multipart payload

This example shows how DataWeave iterates through all the parts of the payload and processes the each part individually.

=== Source
[source,dataweave,linenums]
```

%dw 2.0
output application/json
var multi = '--34b21
Content-Disposition: form-data; name="text"
Content-Type: text/plain

Book
--34b21
Content-Disposition: form-data; name="file1"; filename="a.json"
Content-Type: application/json

{
"title":"Java 8 in Action",
"author":"Mario Fusco",
"year":2014
}
--34b21
Content-Disposition: form-data; name="file2"; filename="a.html"
Content-Type: text/html

<!DOCTYPE html>
<title>
Available for download!
</title>
--34b21--'
var parsed = read(multi, "multipart/form-data", {boundary:'34b21'})
---
parsed.parts mapObject ((value, key, index) -> {(index): key})
```text

=== Output
[source,json,linenums]
```

{
  "0": "text",
  "1": "file1",
  "2": "file2"
}
```text

[[example5]]
=== Example: Using ^mediaType and ^mimeType Metadata Selectors

The `^mimeType` selector returns the MIME type of a value without parameters, for example, `application/json`. The `^mediaType` selector, by contrast, provides the MIME type and any other parameters related to it, for example, `application/json;charset=UTF-16`.

The following example shows how to transform multipart inputs into multipart outputs with a different format. The DataWeave script uses both the `^mimeType` and `^mediaType` selectors to generate the new multipart content.

=== Input
The multipart input has more than one Content-Type. In this case `application/json` and `application/csv` including a non-standard separator:

[source,text,linenums]
```

```text
Content-Type: application/json
Content-Disposition: form-data; name="order"

{
"name": "order1",
"id": 123,
"content": "orderContent"
}
```

Content-Type: application/csv;separator=.
Content-Disposition: form-data; name="partner"

partnerName.id
mulesoft.1
```text
```

#### Source

The DataWeave script transforms the multipart input into multipart output by defining `output multipart/form-data` MIME type. The multipart output data contains two parts:

- `orderAck` +

Contains a text with an acknowledgement of the receipt of an order. The Content-Type is `text/plain`.  The ^mimeType` selector becomes useful to log the Content-Type as part of the message.

- `partner` +

Contains the original partner itself. Notice that this time, the Content-Type is `payload.parts..^mediaType`. The ^mediaType selector includes also the separator, that parses the `application/csv` content.

```dataweave
%dw 2.0
input payload multipart boundary='boundary1'
output multipart boundary='test2'
---
{
  parts : {
    orderAck : {
      headers : {
        "Content-Type": "text/plain"
      },
      content : "Order payload of type " ++ payload.parts.order.content.^mimeType ++ " and id " ++ (payload.parts.order.content.id as String) ++ " received. Receipt available."
    },
    partner: {
      headers : {
        "Content-Type": payload.parts.partner.content.^mediaType
      },
      content : payload.parts.partner.content
    }
  }
}
```

#### Output

```text
--test2
Content-Type: text/plain
Content-Disposition: form-data; name="orderAck"

Order payload of type application/json and id 123 received. Receipt available.
--test2
Content-Type: application/csv;separator=.
Content-Disposition: form-data; name="partner"

partnerName.id
mulesoft.1
--test2--
```

### Configuration Properties

DataWeave supports the following configuration properties for this format.

#### Reader Properties

This format accepts properties that provide instructions for reading input data.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `boundary` | `String` | `null` | The multipart `boundary` value, a string to delimit parts. |
| `defaultContentType` | `String` | `'application/octet-stream'` | Sets the default Content-Type to use on parts of the `multipart/*` format. When set, this property takes precedence over the setting for the system property `com.mulesoft.dw.multipart.defaultContentType`. _Introduced in DataWeave 2.3 (2.3.0-20210720) for the August 2021 release of Mule 4.3.0-20210719._ |

#### Writer Properties

This format accepts properties that provide instructions for writing output data.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `boundary` | `String` | `null` | The multipart `boundary` value, a string to delimit parts. |
| `bufferSize` | `Number` | `8192` | Size of the buffer writer, in bytes. The value must be greater than `8`. |
| `deferred` | `Boolean` | `false` | Generates the output as a data stream when set to `true`, and defers the script's execution until the generated content is consumed. Valid values are `true` or `false`. |

### Supported MIME Types

This format supports the following MIME types.

| MIME Type |
|---|
| `multipart/*` |

---

## Binary Format

MIME type: `application/octet-stream`

ID: `binary`

The Binary data format handles binary content, such as an image or PDF. Such content is represented as a `Binary` type.

Note that Binary content is stored into RAM memory.

### Configuration Properties

DataWeave supports the following configuration properties for this format.

#### Reader Properties

There are no reader properties for this format.

#### Writer Properties

This format accepts properties that provide instructions for writing output data.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `bufferSize` | `Number` | `8192` | Size of the buffer writer, in bytes. The value must be greater than `8`. |
| `deferred` | `Boolean` | `false` | Generates the output as a data stream when set to `true`, and defers the script's execution until the generated content is consumed. Valid values are `true` or `false`. |

### Supported MIME Types

This format supports the following MIME types.

| MIME Type |
|---|
| `application/octet-stream` |
| `application/x-binary` |
