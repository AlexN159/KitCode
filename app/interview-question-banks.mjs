/** Static multiple-choice banks for local interview practice. */

import {
  javaInterviewQuestionSupplement,
  machineLearningInterviewQuestionSupplement,
  sqlInterviewQuestionSupplement,
} from "./interview-question-supplements.mjs";

const supplementsByPrefix = {
  "sql-interview": sqlInterviewQuestionSupplement,
  "java-interview": javaInterviewQuestionSupplement,
  "ml-interview": machineLearningInterviewQuestionSupplement,
};

function buildQuestionBank(prefix, questions) {
  const completeQuestions = [
    ...questions,
    ...(supplementsByPrefix[prefix] ?? []),
  ];
  return Object.freeze(
    completeQuestions.map((question, index) =>
      Object.freeze({
        id: `${prefix}-${String(index + 1).padStart(3, "0")}`,
        title: question.question.replace(/\?$/, ""),
        ...question,
        options: Object.freeze([...question.options]),
      }),
    ),
  );
}

export const sqlInterviewQuestions = buildQuestionBank("sql-interview", [
  {
    topic: "Filtering",
    difficulty: "Easy",
    question: "What is the main difference between WHERE and HAVING?",
    options: [
      "WHERE filters rows before grouping; HAVING filters groups after aggregation",
      "WHERE filters groups; HAVING filters individual rows",
      "HAVING can be used only when there is no GROUP BY",
      "They are interchangeable in every query",
    ],
    correctIndex: 0,
    explanation:
      "WHERE removes input rows before GROUP BY and aggregate evaluation. HAVING applies conditions to the grouped result, so it can filter on aggregate expressions such as COUNT(*).",
  },
  {
    topic: "NULL",
    difficulty: "Easy",
    question: "How should a query test whether a column value is NULL?",
    options: ["column = NULL", "column IS NULL", "column == NULL", "NULL(column)"],
    correctIndex: 1,
    explanation:
      "NULL represents an unknown value and is tested with IS NULL or IS NOT NULL. Equality comparisons with NULL evaluate to UNKNOWN rather than TRUE.",
  },
  {
    topic: "NULL",
    difficulty: "Easy",
    question: "What does COALESCE(a, b, c) return?",
    options: [
      "The first non-NULL argument",
      "The last non-NULL argument",
      "The first argument only when all arguments are NULL",
      "The number of non-NULL arguments",
    ],
    correctIndex: 0,
    explanation:
      "COALESCE evaluates its arguments from left to right and returns the first value that is not NULL. It returns NULL only if every argument is NULL.",
  },
  {
    topic: "Joins",
    difficulty: "Easy",
    question: "What does a LEFT JOIN preserve from its left input?",
    options: [
      "Only rows that match the right table",
      "Every left row, using NULLs when no right row matches",
      "Only duplicate rows",
      "Every right row, using NULLs when no left row matches",
    ],
    correctIndex: 1,
    explanation:
      "A LEFT JOIN returns all rows from the left relation. When its ON condition finds no right-side match, the right-side columns are NULL-extended.",
  },
  {
    topic: "Joins",
    difficulty: "Intermediate",
    question: "Why can a right-table predicate in WHERE accidentally turn a LEFT JOIN into an INNER JOIN?",
    options: [
      "WHERE always changes the join algorithm",
      "The predicate rejects the NULL-extended unmatched rows",
      "LEFT JOIN cannot use predicates",
      "WHERE automatically swaps the two tables",
    ],
    correctIndex: 1,
    explanation:
      "Unmatched right-side columns are NULL. A WHERE condition such as right.status = 'active' is not TRUE for those rows, so they are removed; placing the condition in ON can preserve them.",
  },
  {
    topic: "Joins",
    difficulty: "Intermediate",
    question: "If one customer matches three orders, how many joined rows does an INNER JOIN produce for that customer?",
    options: ["One", "Two", "Three", "It always raises an error"],
    correctIndex: 2,
    explanation:
      "A join emits a row for each matching pair. One customer row combined with three matching order rows therefore produces three result rows.",
  },
  {
    topic: "Sets",
    difficulty: "Easy",
    question: "How does UNION ALL differ from UNION?",
    options: [
      "UNION ALL keeps duplicates, while UNION removes them",
      "UNION ALL sorts rows, while UNION never sorts",
      "UNION ALL requires identical values in both inputs",
      "UNION ALL can combine different column counts",
    ],
    correctIndex: 0,
    explanation:
      "Both operands need compatible columns, but UNION performs duplicate elimination while UNION ALL retains every row. Avoiding deduplication often makes UNION ALL cheaper.",
  },
  {
    topic: "Aggregation",
    difficulty: "Easy",
    question: "What does COUNT(column_name) omit that COUNT(*) includes?",
    options: ["Duplicate values", "Rows where that column is NULL", "Zero values", "Empty strings"],
    correctIndex: 1,
    explanation:
      "COUNT(*) counts result rows. COUNT(expression) counts only rows where its expression is not NULL, although duplicates, zeroes, and usually empty strings still count.",
  },
  {
    topic: "Aggregation",
    difficulty: "Intermediate",
    question: "Why must a selected non-aggregate column usually appear in GROUP BY?",
    options: [
      "To define a single unambiguous value for each output group",
      "To force the database to use an index",
      "To remove NULL values",
      "To convert it into a numeric value",
    ],
    correctIndex: 0,
    explanation:
      "Each output row represents a group. A non-aggregated selected expression must identify the group's value, subject to dialect rules and recognized functional dependencies.",
  },
  {
    topic: "Window functions",
    difficulty: "Easy",
    question: "What is a key difference between a window function and GROUP BY?",
    options: [
      "Window functions preserve input-row detail while computing across related rows",
      "Window functions can never calculate aggregates",
      "GROUP BY always preserves every input row",
      "Window functions work only on text columns",
    ],
    correctIndex: 0,
    explanation:
      "GROUP BY normally collapses rows into one row per group. A window function calculates over a partition while retaining a result row for each input row.",
  },
  {
    topic: "Window functions",
    difficulty: "Intermediate",
    question: "How does DENSE_RANK differ from ROW_NUMBER when ORDER BY values tie?",
    options: [
      "DENSE_RANK gives tied rows the same rank; ROW_NUMBER still assigns unique numbers",
      "ROW_NUMBER gives tied rows the same number; DENSE_RANK does not",
      "DENSE_RANK removes tied rows",
      "There is no difference",
    ],
    correctIndex: 0,
    explanation:
      "ROW_NUMBER assigns a distinct sequence position to every row, with tie order requiring an extra tiebreaker for determinism. DENSE_RANK shares ranks across ties without gaps.",
  },
  {
    topic: "Window functions",
    difficulty: "Intermediate",
    question: "Which window expression most directly produces a running total?",
    options: [
      "SUM(amount) OVER (ORDER BY occurred_at ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)",
      "SUM(amount) GROUP BY occurred_at",
      "COUNT(amount) OVER ()",
      "ORDER BY SUM(amount)",
    ],
    correctIndex: 0,
    explanation:
      "An ordered SUM window with a frame from the start through the current row accumulates values in sequence. An explicit ROWS frame also makes peer-row behavior clear.",
  },
  {
    topic: "Subqueries and CTEs",
    difficulty: "Easy",
    question: "What is a common reason to use a CTE introduced by WITH?",
    options: [
      "To name and structure an intermediate query result",
      "To permanently store rows on disk",
      "To create an index automatically",
      "To commit a transaction",
    ],
    correctIndex: 0,
    explanation:
      "A common table expression gives a query expression a name within one statement. It can improve readability and support recursive queries, but is not itself permanent storage.",
  },
  {
    topic: "Subqueries and CTEs",
    difficulty: "Intermediate",
    question: "What makes a subquery correlated?",
    options: [
      "It references a column from an outer query scope",
      "It contains GROUP BY",
      "It returns more than one column",
      "It appears in the FROM clause",
    ],
    correctIndex: 0,
    explanation:
      "A correlated subquery depends on values from the current outer row. Optimizers may decorrelate it, but its logical evaluation is tied to the outer query scope.",
  },
  {
    topic: "Subqueries and CTEs",
    difficulty: "Intermediate",
    question: "When is EXISTS especially suitable?",
    options: [
      "When testing whether at least one related row satisfies a condition",
      "When returning every column from a related table",
      "When sorting the final result",
      "When converting text to a date",
    ],
    correctIndex: 0,
    explanation:
      "EXISTS expresses a semi-join-style existence test and can stop logically after a match. It also avoids multiplying outer rows as a regular join might.",
  },
  {
    topic: "Subqueries and CTEs",
    difficulty: "Advanced",
    question: "What is a classic use for a recursive CTE?",
    options: [
      "Traversing hierarchical parent-child data",
      "Changing a column's data type",
      "Granting a user permission",
      "Creating a transaction savepoint",
    ],
    correctIndex: 0,
    explanation:
      "A recursive CTE combines an anchor query with a recursive member, making it useful for trees, graphs, organizational hierarchies, and sequence generation.",
  },
  {
    topic: "Keys and constraints",
    difficulty: "Easy",
    question: "What does a primary key guarantee?",
    options: [
      "A unique, non-NULL identifier for each row",
      "Rows are physically stored in key order in every database",
      "Every query uses the key's index",
      "The table can contain only one other constraint",
    ],
    correctIndex: 0,
    explanation:
      "A primary key enforces entity identity through uniqueness and non-NULL values. Its physical storage and indexing implementation vary across database systems.",
  },
  {
    topic: "Keys and constraints",
    difficulty: "Easy",
    question: "What is the purpose of a foreign key?",
    options: [
      "To enforce allowed relationships between child and parent rows",
      "To encrypt a column",
      "To make every join faster",
      "To prevent all parent-row updates",
    ],
    correctIndex: 0,
    explanation:
      "A foreign key enforces referential integrity: a child reference must match an allowed parent key, unless it is NULL when permitted. Update and delete actions are configurable.",
  },
  {
    topic: "Data modeling",
    difficulty: "Intermediate",
    question: "What problem does third normal form primarily reduce?",
    options: [
      "Update anomalies caused by non-key attributes depending on other non-key attributes",
      "Slow network connections",
      "Missing indexes on every column",
      "The need for transactions",
    ],
    correctIndex: 0,
    explanation:
      "Third normal form aims to remove inappropriate transitive dependencies, reducing redundant facts and the insert, update, and delete anomalies they can cause.",
  },
  {
    topic: "Data modeling",
    difficulty: "Intermediate",
    question: "Why might a read-heavy analytical system deliberately denormalize data?",
    options: [
      "To reduce joins and simplify common reads at the cost of redundancy",
      "To guarantee that duplicate facts can never diverge",
      "To eliminate all storage costs",
      "To disable constraints automatically",
    ],
    correctIndex: 0,
    explanation:
      "Denormalization can precombine or duplicate facts to speed frequent reads. The tradeoff is extra storage and more work to keep redundant data consistent.",
  },
  {
    topic: "Indexes",
    difficulty: "Easy",
    question: "Which workload most clearly benefits from an index on a column?",
    options: [
      "Selective lookups and joins using that column",
      "Every bulk insert regardless of later reads",
      "Queries that never reference the column",
      "Dropping the table",
    ],
    correctIndex: 0,
    explanation:
      "Indexes can avoid scanning all rows for selective predicates, joins, or ordered access. They consume space and add maintenance cost to writes, so they are workload-dependent.",
  },
  {
    topic: "Indexes",
    difficulty: "Intermediate",
    question: "For a typical B-tree index on (last_name, first_name), which predicate best uses its leading order?",
    options: [
      "last_name = 'Ng'",
      "first_name = 'Ava' with no last_name condition",
      "UPPER(first_name) = 'AVA' only",
      "A condition on an unrelated column",
    ],
    correctIndex: 0,
    explanation:
      "Composite B-tree access commonly follows the leftmost prefix. The leading last_name column can support a seek, while first_name alone generally cannot use that ordering as effectively.",
  },
  {
    topic: "Indexes",
    difficulty: "Intermediate",
    question: "What is a covering index for a particular query?",
    options: [
      "An index containing all columns needed to satisfy that query",
      "An index that includes every table in the database",
      "A backup copy of a primary key",
      "An index used only during transactions",
    ],
    correctIndex: 0,
    explanation:
      "A covering index contains the query's required filter, join, and output values, allowing some engines to avoid an extra lookup to the base table.",
  },
  {
    topic: "Performance",
    difficulty: "Intermediate",
    question: "Which predicate is generally more sargable for an indexed created_at timestamp?",
    options: [
      "created_at >= '2026-01-01' AND created_at < '2026-02-01'",
      "YEAR(created_at) = 2026 AND MONTH(created_at) = 1",
      "CAST(created_at AS TEXT) LIKE '2026-01%'",
      "created_at + INTERVAL '0 day' >= '2026-01-01'",
    ],
    correctIndex: 0,
    explanation:
      "A direct range predicate lets an optimizer match the indexed values. Wrapping the indexed column in functions often prevents a normal index seek unless a matching expression index exists.",
  },
  {
    topic: "Performance",
    difficulty: "Easy",
    question: "What does an EXPLAIN plan help an engineer inspect?",
    options: [
      "The optimizer's access paths, join strategies, and row estimates",
      "The table's business requirements",
      "The user's plaintext password",
      "Only the final result rows",
    ],
    correctIndex: 0,
    explanation:
      "EXPLAIN exposes how the database plans to execute a statement, including scans, indexes, joins, sorts, and estimates. Runtime variants can also report actual execution statistics.",
  },
  {
    topic: "Performance",
    difficulty: "Advanced",
    question: "Why can stale table statistics lead to a poor query plan?",
    options: [
      "The optimizer may misestimate row counts and choose unsuitable joins or access paths",
      "Statistics directly delete old rows",
      "Statistics disable SQL parsing",
      "The database must then ignore every index",
    ],
    correctIndex: 0,
    explanation:
      "Cost-based optimization depends on cardinality and distribution estimates. Stale statistics can distort those estimates and make an otherwise rational cost comparison choose badly.",
  },
  {
    topic: "Transactions",
    difficulty: "Easy",
    question: "In ACID, what does atomicity mean?",
    options: [
      "A transaction's changes succeed as one unit or are rolled back as one unit",
      "Every transaction runs without concurrency",
      "Data is always stored in alphabetical order",
      "Queries cannot fail",
    ],
    correctIndex: 0,
    explanation:
      "Atomicity gives a transaction all-or-nothing behavior. It does not by itself define concurrency isolation, durability after commit, or application correctness.",
  },
  {
    topic: "Transactions",
    difficulty: "Intermediate",
    question: "What is a dirty read?",
    options: [
      "Reading another transaction's changes before they commit",
      "Reading the same committed row twice",
      "Reading a row without an index",
      "Reading a row containing NULL",
    ],
    correctIndex: 0,
    explanation:
      "A dirty read observes uncommitted data that may later be rolled back. Isolation levels differ in which anomalies they prevent.",
  },
  {
    topic: "Transactions",
    difficulty: "Intermediate",
    question: "What is a lost update anomaly?",
    options: [
      "One concurrent write overwrites another based on a stale value",
      "A committed row disappears from a backup",
      "An UPDATE has no WHERE clause",
      "A query returns rows in a different order",
    ],
    correctIndex: 0,
    explanation:
      "A lost update can occur when concurrent transactions read the same starting value and later write results that overwrite one another. Locking, atomic updates, or optimistic version checks can prevent it.",
  },
  {
    topic: "Transactions",
    difficulty: "Intermediate",
    question: "What does a transaction savepoint provide?",
    options: [
      "A point to which part of the current transaction can be rolled back",
      "A permanent database backup",
      "A new user account",
      "Automatic replication",
    ],
    correctIndex: 0,
    explanation:
      "A savepoint marks an intermediate transaction state. Rolling back to it can undo later work without necessarily aborting the entire transaction.",
  },
  {
    topic: "Query semantics",
    difficulty: "Intermediate",
    question: "Which sequence best reflects SQL's logical query processing order?",
    options: [
      "FROM/JOIN, WHERE, GROUP BY, HAVING, SELECT, ORDER BY",
      "SELECT, ORDER BY, FROM, WHERE, GROUP BY, HAVING",
      "WHERE, SELECT, FROM, HAVING, JOIN, ORDER BY",
      "ORDER BY, FROM, SELECT, GROUP BY, WHERE, HAVING",
    ],
    correctIndex: 0,
    explanation:
      "SQL is written starting with SELECT, but its logical phases begin with FROM and JOIN, then filtering and grouping, followed by projection and ordering. Physical execution may be optimized differently.",
  },
  {
    topic: "Query semantics",
    difficulty: "Intermediate",
    question: "Why should a LIMIT or TOP query normally include ORDER BY when selecting a deterministic subset?",
    options: [
      "Without ORDER BY, SQL does not guarantee which qualifying rows are returned",
      "LIMIT is invalid syntax without ORDER BY in every dialect",
      "ORDER BY removes duplicates",
      "ORDER BY makes every query constant time",
    ],
    correctIndex: 0,
    explanation:
      "Relations have no guaranteed presentation order. Without an ORDER BY that fully breaks ties, the chosen subset can change with plans, data layout, or concurrent activity.",
  },
  {
    topic: "Query patterns",
    difficulty: "Advanced",
    question: "Which pattern is commonly used to return the highest-paid employee in each department while retaining employee columns?",
    options: [
      "Assign ROW_NUMBER() over each department ordered by salary descending, then keep row 1",
      "Apply one global ORDER BY salary and keep one row",
      "GROUP BY employee_id only",
      "Use DISTINCT on salary only",
    ],
    correctIndex: 0,
    explanation:
      "A partitioned ranking window solves top-N-per-group while retaining complete row detail. A deliberate secondary ordering rule is needed if ties must be resolved deterministically.",
  },
  {
    topic: "Query patterns",
    difficulty: "Advanced",
    question: "Why is NOT EXISTS often safer than NOT IN when the subquery can return NULL?",
    options: [
      "NULL inside NOT IN can make comparisons UNKNOWN and unexpectedly return no rows",
      "NOT EXISTS always sorts the subquery",
      "NOT IN cannot compare numeric values",
      "NOT EXISTS permanently removes matching rows",
    ],
    correctIndex: 0,
    explanation:
      "SQL's three-valued logic makes x NOT IN (..., NULL) evaluate to UNKNOWN for candidates without a match. A correlated NOT EXISTS expresses the anti-join without that NULL trap.",
  },
  {
    topic: "Security",
    difficulty: "Easy",
    question: "What is the primary defense against SQL injection in application queries?",
    options: [
      "Parameterized queries with values bound separately from SQL text",
      "Removing spaces from user input",
      "Escaping only quotation marks by hand",
      "Hiding database error messages only",
    ],
    correctIndex: 0,
    explanation:
      "Parameters keep untrusted values out of the SQL grammar, preventing them from becoming executable syntax. Least-privilege database accounts add defense in depth.",
  },
  {
    topic: "Schema objects",
    difficulty: "Intermediate",
    question: "How does a materialized view generally differ from a regular view?",
    options: [
      "It stores query results and must be refreshed to reflect source changes",
      "It can never be queried",
      "It contains no SQL definition",
      "It is identical in every database product",
    ],
    correctIndex: 0,
    explanation:
      "A regular view normally stores a query definition, while a materialized view persists its result for faster reads. Refresh behavior and feature support vary by database.",
  },
  {
    topic: "DML and DDL",
    difficulty: "Intermediate",
    question: "Which statement about DELETE, TRUNCATE, and DROP is most portable?",
    options: [
      "DELETE removes rows, TRUNCATE removes all rows as a table operation, and DROP removes the table object",
      "All three always have identical logging and rollback behavior",
      "DROP keeps the schema but removes selected rows",
      "TRUNCATE accepts a WHERE clause in every major database",
    ],
    correctIndex: 0,
    explanation:
      "Their broad intent is portable, but locking, identity reset, triggers, logging, permissions, and transactional rollback differ by database product. Those details should be stated with a dialect.",
  },
  {
    topic: "Data warehousing",
    difficulty: "Intermediate",
    question: "In a star schema, what does a fact table usually contain?",
    options: [
      "Measurements at a declared grain plus keys to descriptive dimensions",
      "Only free-form documentation",
      "One row for every database user",
      "Only unique dimension labels",
    ],
    correctIndex: 0,
    explanation:
      "A fact table records business events or snapshots at a specific grain, with numeric measures and foreign keys to dimension tables that provide descriptive context.",
  },
]);

export const javaInterviewQuestions = buildQuestionBank("java-interview", [
  {
    topic: "Platform",
    difficulty: "Easy",
    question: "How do the JDK, JVM, and Java runtime relate?",
    options: [
      "The JDK adds development tools; the runtime supplies libraries and the JVM; the JVM executes bytecode",
      "The JVM compiles Java source but cannot execute bytecode",
      "The JDK is only a text editor",
      "They are three names for exactly the same component",
    ],
    correctIndex: 0,
    explanation:
      "The JVM executes Java bytecode, while the runtime also includes libraries and supporting components. A JDK provides that runtime plus tools such as javac, javadoc, and debuggers.",
  },
  {
    topic: "Objects",
    difficulty: "Easy",
    question: "For object references, what is the usual difference between == and equals()?",
    options: [
      "== compares reference identity; equals() can define logical value equality",
      "== calls equals() automatically",
      "equals() always compares memory addresses",
      "== works only with strings",
    ],
    correctIndex: 0,
    explanation:
      "For references, == asks whether both operands point to the same object. Object.equals defaults to identity too, but classes can override it to represent value equality.",
  },
  {
    topic: "Objects",
    difficulty: "Intermediate",
    question: "What must be true when a class overrides equals()?",
    options: [
      "Equal objects must return the same hashCode()",
      "Unequal objects must always have different hash codes",
      "equals() must compare object identity only",
      "hashCode() must return a random value",
    ],
    correctIndex: 0,
    explanation:
      "The equality contract requires equal objects to have equal hash codes so hash-based collections can find them consistently. Hash collisions between unequal objects are allowed.",
  },
  {
    topic: "Strings",
    difficulty: "Easy",
    question: "Why is String immutable in Java?",
    options: [
      "Operations create new string values instead of changing an existing String object",
      "A String can contain only final characters",
      "String variables can never be reassigned",
      "The JVM stores every String in one fixed location",
    ],
    correctIndex: 0,
    explanation:
      "A String object's character sequence cannot change after construction, though a variable may point to a different String. Immutability supports safe sharing, pooling, security, and cached hashes.",
  },
  {
    topic: "Strings",
    difficulty: "Easy",
    question: "When is StringBuilder normally preferable to repeated String concatenation?",
    options: [
      "When building a string through many mutations, especially in a loop",
      "When a compile-time constant joins two literals",
      "When value immutability is the only requirement",
      "When the result must be a number",
    ],
    correctIndex: 0,
    explanation:
      "StringBuilder maintains a mutable character buffer and avoids producing many intermediate String objects. Modern compilers already optimize simple one-expression concatenations.",
  },
  {
    topic: "Language semantics",
    difficulty: "Easy",
    question: "Is Java pass-by-reference for objects?",
    options: [
      "No; Java passes a copy of the reference value",
      "Yes; a method can rebind the caller's variable directly",
      "Only constructors use pass-by-value",
      "Only immutable objects are passed by value",
    ],
    correctIndex: 0,
    explanation:
      "Java is pass-by-value. For an object argument, the copied value is a reference, so a method can mutate the referenced object but cannot reassign the caller's variable itself.",
  },
  {
    topic: "Language semantics",
    difficulty: "Easy",
    question: "What does final mean on a reference variable?",
    options: [
      "The variable cannot be reassigned after initialization, but the referenced object may still be mutable",
      "The object becomes deeply immutable",
      "The object cannot be garbage-collected",
      "The variable becomes globally accessible",
    ],
    correctIndex: 0,
    explanation:
      "final prevents another assignment to that variable. It does not recursively freeze the object's fields or the objects reachable from it.",
  },
  {
    topic: "Language semantics",
    difficulty: "Easy",
    question: "What does static mean for a field?",
    options: [
      "The field belongs to the class rather than to each individual instance",
      "The field can never change",
      "The field is stored on disk",
      "The field is visible only inside constructors",
    ],
    correctIndex: 0,
    explanation:
      "A static field is associated with the class and shared through its class loader context. final is the separate modifier that prevents reassignment.",
  },
  {
    topic: "OOP",
    difficulty: "Easy",
    question: "What is method overloading?",
    options: [
      "Defining methods with the same name but different parameter lists",
      "Replacing a superclass method with the same signature in a subclass",
      "Calling a private method from two threads",
      "Giving one method two return statements",
    ],
    correctIndex: 0,
    explanation:
      "Overloading is resolved at compile time from the declared argument types and applicable signatures. A return type alone is not enough to create a distinct overload.",
  },
  {
    topic: "OOP",
    difficulty: "Easy",
    question: "What is method overriding?",
    options: [
      "A subclass supplies an instance-method implementation compatible with an inherited signature",
      "Two methods in one class have different parameter counts",
      "A static field hides an instance field",
      "A method catches an exception",
    ],
    correctIndex: 0,
    explanation:
      "Overriding enables runtime polymorphism: the implementation is selected from the actual object's class. @Override lets the compiler verify that the intended override is valid.",
  },
  {
    topic: "OOP",
    difficulty: "Intermediate",
    question: "Why is composition often preferred over inheritance for code reuse?",
    options: [
      "It can reduce coupling and model behavior without forcing an is-a relationship",
      "Java forbids inheriting implemented methods",
      "Composition makes every method static",
      "Inheritance cannot support polymorphism",
    ],
    correctIndex: 0,
    explanation:
      "Composition delegates to contained collaborators and can keep implementations replaceable. Inheritance is appropriate for genuine substitutability, not merely to borrow implementation.",
  },
  {
    topic: "OOP",
    difficulty: "Intermediate",
    question: "Which distinction between an interface and an abstract class is accurate?",
    options: [
      "A class can implement multiple interfaces but extend only one class",
      "Interfaces can never contain implemented methods",
      "Abstract classes cannot have constructors",
      "Interfaces can hold mutable per-instance fields",
    ],
    correctIndex: 0,
    explanation:
      "Java supports multiple interface implementation but single class inheritance. Interfaces can have default and static methods, while abstract classes can hold instance state and constructors.",
  },
  {
    topic: "OOP",
    difficulty: "Intermediate",
    question: "What problem do default methods in interfaces primarily address?",
    options: [
      "Evolving an interface with reusable behavior while preserving compatibility for many implementers",
      "Allowing interfaces to store mutable instance state",
      "Replacing every abstract class",
      "Making all implementations thread-safe",
    ],
    correctIndex: 0,
    explanation:
      "Default methods let an interface add an implemented operation without immediately breaking every existing implementation. Conflict and inheritance rules still apply.",
  },
  {
    topic: "OOP",
    difficulty: "Intermediate",
    question: "What does the Liskov substitution principle require in practical terms?",
    options: [
      "Subtype objects should honor the behavioral expectations of the base type",
      "Every subclass must add new public methods",
      "Base classes must be final",
      "Only interfaces may be used as variable types",
    ],
    correctIndex: 0,
    explanation:
      "Code written against a base abstraction should continue to behave correctly when given a subtype. A subtype should not strengthen preconditions or violate promised invariants.",
  },
  {
    topic: "Exceptions",
    difficulty: "Easy",
    question: "How do checked exceptions differ from unchecked exceptions?",
    options: [
      "Checked exceptions must generally be caught or declared; RuntimeException subclasses do not",
      "Unchecked exceptions can never be caught",
      "Checked exceptions always terminate the JVM",
      "Only checked exceptions have stack traces",
    ],
    correctIndex: 0,
    explanation:
      "The compiler enforces handling or declaration for checked exception types. RuntimeException and Error hierarchies are unchecked, though they can still be caught where appropriate.",
  },
  {
    topic: "Exceptions",
    difficulty: "Easy",
    question: "What is the main benefit of try-with-resources?",
    options: [
      "It closes declared AutoCloseable resources automatically, including on exceptions",
      "It retries failed I/O forever",
      "It prevents every checked exception",
      "It makes a resource globally shared",
    ],
    correctIndex: 0,
    explanation:
      "try-with-resources gives deterministic cleanup in reverse declaration order. If closing also fails, those errors can be retained as suppressed exceptions.",
  },
  {
    topic: "Exceptions",
    difficulty: "Intermediate",
    question: "Why is catching Exception and ignoring it usually harmful?",
    options: [
      "It hides failures and can let execution continue with invalid state",
      "The compiler converts it to an Error",
      "It makes the catch block run twice",
      "Exception cannot be caught in Java",
    ],
    correctIndex: 0,
    explanation:
      "Swallowing broad exceptions destroys diagnostic context and obscures recovery behavior. Catch narrowly where the code can add context, recover, or translate the failure meaningfully.",
  },
  {
    topic: "Generics",
    difficulty: "Intermediate",
    question: "Why is List<Integer> not a subtype of List<Number>?",
    options: [
      "Java generics are invariant, preventing unsafe insertion of another Number subtype",
      "Integer does not extend Number",
      "Lists cannot use numeric types",
      "Generic lists are always immutable",
    ],
    correctIndex: 0,
    explanation:
      "If List<Integer> were a List<Number>, code could insert a Double and break the original list's promise. Wildcards express safe variance at an API boundary.",
  },
  {
    topic: "Generics",
    difficulty: "Intermediate",
    question: "What does the PECS guideline mean for generic wildcards?",
    options: [
      "Use extends for a producer and super for a consumer",
      "Use extends for every mutable collection",
      "Use super only for return types",
      "Avoid all bounded wildcards",
    ],
    correctIndex: 0,
    explanation:
      "A source that produces T values can often be ? extends T, while a destination that consumes T can be ? super T. This describes use-site variance safely.",
  },
  {
    topic: "Generics",
    difficulty: "Advanced",
    question: "What is type erasure in Java generics?",
    options: [
      "Most generic type arguments are removed from runtime representation, with casts and bounds inserted as needed",
      "The compiler deletes every generic method",
      "Generic objects cannot exist on the heap",
      "All type checking is postponed until runtime",
    ],
    correctIndex: 0,
    explanation:
      "Java generics are primarily a compile-time feature implemented through erasure. This explains restrictions such as new T(), generic arrays, and many runtime instanceof checks.",
  },
  {
    topic: "Collections",
    difficulty: "Easy",
    question: "Which collection contract best describes a Set?",
    options: [
      "It contains no duplicate elements according to its equality rules",
      "It always keeps elements sorted",
      "It maps every key to a value",
      "It allows access only by numeric index",
    ],
    correctIndex: 0,
    explanation:
      "Set models membership without duplicates. Ordering differs by implementation: HashSet has no iteration-order guarantee, LinkedHashSet preserves insertion order, and TreeSet sorts.",
  },
  {
    topic: "Collections",
    difficulty: "Easy",
    question: "Why is ArrayList usually a good default List implementation?",
    options: [
      "It offers compact storage and fast indexed access with good iteration locality",
      "Every insertion is constant time in every position",
      "It is automatically thread-safe",
      "It stores elements in sorted order",
    ],
    correctIndex: 0,
    explanation:
      "ArrayList uses a resizable array, giving fast random access and cache-friendly traversal. Middle insertions and removals can require shifting elements.",
  },
  {
    topic: "Collections",
    difficulty: "Intermediate",
    question: "What is the expected average lookup complexity of a well-behaved HashMap?",
    options: ["O(1)", "O(log n) in every case", "O(n log n)", "O(2^n)"],
    correctIndex: 0,
    explanation:
      "With well-distributed hashes and normal load, HashMap get and put are expected constant time. Collisions and adversarial distributions can worsen behavior, with modern implementations treeifying some large buckets.",
  },
  {
    topic: "Collections",
    difficulty: "Intermediate",
    question: "Why is mutating a HashMap key after insertion dangerous?",
    options: [
      "If equality or hashCode changes, the entry may no longer be found in its original bucket",
      "HashMap freezes every key automatically",
      "The map immediately becomes a TreeMap",
      "Only primitive keys are legal",
    ],
    correctIndex: 0,
    explanation:
      "Hash-based lookup assumes the key's hash and equality-relevant state remain stable while stored. Immutable key types are therefore the safest choice.",
  },
  {
    topic: "Collections",
    difficulty: "Intermediate",
    question: "What does ConcurrentHashMap provide that HashMap does not?",
    options: [
      "Thread-safe concurrent access without one external lock around every operation",
      "A guarantee that compound read-then-write sequences are automatically atomic",
      "Sorted keys",
      "Support for null keys and values",
    ],
    correctIndex: 0,
    explanation:
      "ConcurrentHashMap coordinates concurrent operations and offers atomic methods such as compute and putIfAbsent. Multi-step logic still needs an appropriate atomic method or additional coordination.",
  },
  {
    topic: "Streams",
    difficulty: "Easy",
    question: "When do intermediate Stream operations such as map and filter normally execute?",
    options: [
      "Lazily when a terminal operation consumes the pipeline",
      "Immediately when the stream is declared",
      "Only after the JVM exits",
      "Only on a background thread",
    ],
    correctIndex: 0,
    explanation:
      "Intermediate operations build a lazy pipeline. A terminal operation initiates traversal, allowing fusion and short-circuiting rather than materializing every stage.",
  },
  {
    topic: "Streams",
    difficulty: "Intermediate",
    question: "How does flatMap differ from map in a Stream pipeline?",
    options: [
      "flatMap maps each element to a stream-like result and flattens those results into one stream",
      "flatMap always sorts the stream",
      "map can return only primitive values",
      "flatMap disables lazy evaluation",
    ],
    correctIndex: 0,
    explanation:
      "map produces one output value per input value, which can lead to nested containers. flatMap both transforms and flattens one level, such as Stream<List<T>> into Stream<T>.",
  },
  {
    topic: "Streams",
    difficulty: "Intermediate",
    question: "Why should stream operations generally avoid shared mutable side effects?",
    options: [
      "They make behavior harder to reason about and unsafe under parallel execution",
      "Streams prohibit calling methods",
      "Side effects always cause a compilation error",
      "They force every stream to be infinite",
    ],
    correctIndex: 0,
    explanation:
      "Stateless, non-interfering operations preserve pipeline semantics and parallel safety. Use collectors and reductions instead of mutating shared external containers where practical.",
  },
  {
    topic: "Functional Java",
    difficulty: "Intermediate",
    question: "What does effectively final mean for a local variable captured by a lambda?",
    options: [
      "It is assigned once and never reassigned, even if the final keyword is omitted",
      "Its referenced object is deeply immutable",
      "It is converted into a static field",
      "It can be reassigned only inside the lambda",
    ],
    correctIndex: 0,
    explanation:
      "Captured local variables must be final or effectively final. The restriction concerns reassignment of the variable, not mutation of an object it references.",
  },
  {
    topic: "Functional Java",
    difficulty: "Intermediate",
    question: "What is Optional primarily intended to communicate?",
    options: [
      "A return value may be absent and should be handled explicitly",
      "Every field should replace null with Optional",
      "A computation will run asynchronously",
      "A value is thread-safe",
    ],
    correctIndex: 0,
    explanation:
      "Optional is chiefly a return-type signal for possible absence and supports compositional handling. It is not a universal replacement for every nullable field, parameter, or collection.",
  },
  {
    topic: "Concurrency",
    difficulty: "Easy",
    question: "What does synchronized establish around a correctly shared monitor?",
    options: [
      "Mutual exclusion plus visibility ordering for monitor release and acquisition",
      "Lock-free execution",
      "A new operating-system process",
      "Automatic deadlock prevention",
    ],
    correctIndex: 0,
    explanation:
      "A synchronized block acquires a monitor, allowing one holder at a time, and its unlock/lock relationship provides happens-before visibility. Poor lock design can still deadlock.",
  },
  {
    topic: "Concurrency",
    difficulty: "Intermediate",
    question: "What does volatile guarantee for a field?",
    options: [
      "Visibility and ordering for reads and writes of that field, but not atomicity of compound updates",
      "Every operation on the containing object is atomic",
      "Only one thread can read the field",
      "The field is persisted after a crash",
    ],
    correctIndex: 0,
    explanation:
      "A volatile write happens-before later reads of that field and prevents certain reorderings. An expression such as count++ is still a read-modify-write race.",
  },
  {
    topic: "Concurrency",
    difficulty: "Intermediate",
    question: "Which tool is appropriate for an atomic concurrent counter increment?",
    options: ["AtomicInteger.incrementAndGet()", "A plain int++ with no coordination", "StringBuilder", "Optional<Integer>"],
    correctIndex: 0,
    explanation:
      "AtomicInteger supplies atomic read-modify-write operations using concurrency primitives. A volatile int would make values visible but would not make increment atomic.",
  },
  {
    topic: "Concurrency",
    difficulty: "Advanced",
    question: "Which condition is necessary for a classic deadlock?",
    options: [
      "A circular wait among threads holding resources needed by one another",
      "Every task uses a single immutable value",
      "No thread ever blocks",
      "All locks are acquired in one consistent global order",
    ],
    correctIndex: 0,
    explanation:
      "Circular wait is one Coffman condition for deadlock, alongside mutual exclusion, hold-and-wait, and no preemption. Consistent lock ordering is a common prevention technique.",
  },
  {
    topic: "Concurrency",
    difficulty: "Intermediate",
    question: "What is the main use case for Java virtual threads?",
    options: [
      "Supporting very many mostly blocking tasks with a thread-per-task style",
      "Making CPU-bound algorithms run faster than the available cores",
      "Replacing synchronization semantics",
      "Guaranteeing zero context-switch cost",
    ],
    correctIndex: 0,
    explanation:
      "Virtual threads make large numbers of blocking, I/O-heavy tasks practical while retaining straightforward code. They do not create additional CPU capacity or remove the need for safe shared state.",
  },
  {
    topic: "Modern Java",
    difficulty: "Easy",
    question: "What does a Java record primarily provide?",
    options: [
      "A concise class form for transparent data carriers with generated component API and value methods",
      "A mutable database row with automatic persistence",
      "A class that can extend any concrete superclass",
      "A replacement for every domain object",
    ],
    correctIndex: 0,
    explanation:
      "A record declares a fixed set of components and receives accessors, a canonical constructor, equals, hashCode, and toString. Component references are final, but referenced objects may be mutable.",
  },
  {
    topic: "Modern Java",
    difficulty: "Intermediate",
    question: "What do sealed classes and interfaces control?",
    options: [
      "Which types are permitted to extend or implement them",
      "Which objects may be garbage-collected",
      "Which methods run in parallel",
      "Which fields are serialized",
    ],
    correctIndex: 0,
    explanation:
      "A sealed hierarchy explicitly constrains its direct subtypes. This supports deliberate domain modeling and more exhaustive reasoning in pattern-based code.",
  },
  {
    topic: "JVM",
    difficulty: "Intermediate",
    question: "What makes an object eligible for garbage collection?",
    options: [
      "It is no longer strongly reachable from any live GC root",
      "Its local variable name goes out of alphabetical order",
      "Its class implements AutoCloseable",
      "It has existed for a fixed number of seconds",
    ],
    correctIndex: 0,
    explanation:
      "Modern JVM collectors determine reachability from roots such as live thread stacks and static references. Eligibility does not promise immediate collection or resource cleanup timing.",
  },
  {
    topic: "JVM",
    difficulty: "Advanced",
    question: "Why can a static field contribute to a memory leak in a managed JVM?",
    options: [
      "It may keep an object graph strongly reachable for the lifetime of its class loader",
      "Static fields are allocated outside all memory",
      "The garbage collector ignores every class",
      "Static fields cannot contain references",
    ],
    correctIndex: 0,
    explanation:
      "Garbage collection reclaims unreachable objects, not objects that are merely no longer useful. Long-lived static caches or listeners can accidentally retain large graphs.",
  },
  {
    topic: "Testing and design",
    difficulty: "Intermediate",
    question: "Why does dependency injection often improve unit testability?",
    options: [
      "Collaborators can be supplied explicitly and replaced with controlled test doubles",
      "It makes all production methods private",
      "It removes the need for assertions",
      "It guarantees integration tests always pass",
    ],
    correctIndex: 0,
    explanation:
      "Explicitly supplied dependencies reduce hidden global coupling and let a unit test control boundaries such as clocks, repositories, and network clients.",
  },
  {
    topic: "Testing and design",
    difficulty: "Intermediate",
    question: "What is the main value of an immutable object in concurrent code?",
    options: [
      "It can be shared without races over changing internal state once safely published",
      "It automatically makes every referenced object immutable",
      "It never consumes heap memory",
      "It can be modified without synchronization",
    ],
    correctIndex: 0,
    explanation:
      "An object whose observable state never changes avoids mutation races and is easier to reason about. Deep immutability still requires controlling referenced mutable objects.",
  },
]);

export const machineLearningInterviewQuestions = buildQuestionBank("ml-interview", [
  {
    topic: "Learning basics",
    difficulty: "Easy",
    question: "What is the difference between supervised and unsupervised learning?",
    options: [
      "Supervised learning uses labeled targets; unsupervised learning looks for structure without target labels",
      "Supervised learning never evaluates a loss",
      "Unsupervised learning always predicts a continuous number",
      "They differ only in programming language",
    ],
    correctIndex: 0,
    explanation:
      "Supervised models learn a mapping from inputs to known targets. Unsupervised methods instead seek patterns such as clusters, components, or density structure in unlabeled data.",
  },
  {
    topic: "Linear models",
    difficulty: "Easy",
    question: "What does ordinary linear regression estimate?",
    options: [
      "A linear relationship between features and a continuous target",
      "A probability distribution over tree leaves only",
      "A set of unlabeled clusters",
      "A deterministic class boundary with no fitted parameters",
    ],
    correctIndex: 0,
    explanation:
      "Linear regression fits coefficients so a weighted sum of features approximates a continuous response, commonly by minimizing squared residuals.",
  },
  {
    topic: "Linear models",
    difficulty: "Intermediate",
    question: "Which assumption is needed for ordinary least squares coefficients to have their usual unbiased linear-model interpretation?",
    options: [
      "The errors have zero conditional mean given the features",
      "Every feature is normally distributed",
      "The target contains no noise",
      "All coefficients are positive",
    ],
    correctIndex: 0,
    explanation:
      "A central exogeneity assumption is E[error | X] = 0. Normal errors are relevant to some small-sample inference, but not required simply to fit least squares.",
  },
  {
    topic: "Linear models",
    difficulty: "Intermediate",
    question: "Why is mean squared error especially sensitive to outliers?",
    options: [
      "Squaring makes large residuals contribute disproportionately",
      "It ignores residual magnitude",
      "It clips every residual to one",
      "It uses only the median residual",
    ],
    correctIndex: 0,
    explanation:
      "A residual twice as large contributes four times the squared loss. Robust alternatives such as absolute or Huber loss can reduce extreme-point influence.",
  },
  {
    topic: "Linear models",
    difficulty: "Easy",
    question: "What does logistic regression model for binary classification?",
    options: [
      "The log-odds as a linear function of the features",
      "The target directly with an unconstrained straight line",
      "Only the distance to the nearest neighbor",
      "A hierarchy of decision rules",
    ],
    correctIndex: 0,
    explanation:
      "Logistic regression applies a sigmoid to a linear score, making the log-odds linear and producing probabilities between zero and one.",
  },
  {
    topic: "Optimization",
    difficulty: "Easy",
    question: "What does gradient descent do at each basic update?",
    options: [
      "Moves parameters opposite the loss gradient",
      "Moves parameters in a random direction regardless of loss",
      "Adds more training examples",
      "Removes the model's intercept",
    ],
    correctIndex: 0,
    explanation:
      "The gradient points in the direction of steepest local increase, so subtracting a learning-rate-scaled gradient seeks a lower loss.",
  },
  {
    topic: "Optimization",
    difficulty: "Easy",
    question: "What can happen when the learning rate is much too large?",
    options: [
      "Updates can overshoot and the loss may oscillate or diverge",
      "Training always converges in one step",
      "The model automatically adds regularization",
      "Every gradient becomes exactly zero",
    ],
    correctIndex: 0,
    explanation:
      "An excessive step size can jump across useful descent directions and destabilize optimization. A tiny rate is usually stable but may converge impractically slowly.",
  },
  {
    topic: "Optimization",
    difficulty: "Intermediate",
    question: "How does mini-batch gradient descent differ from full-batch gradient descent?",
    options: [
      "It estimates each update from a subset of training examples",
      "It never uses gradients",
      "It trains only one model parameter",
      "It requires the entire dataset for every update",
    ],
    correctIndex: 0,
    explanation:
      "Mini-batches trade noisier gradient estimates for cheaper, more frequent updates and efficient vectorized hardware use. Full-batch updates use every training example each step.",
  },
  {
    topic: "Optimization",
    difficulty: "Intermediate",
    question: "What problem can vanishing gradients cause in a deep network?",
    options: [
      "Early layers receive extremely small updates and learn slowly",
      "The loss becomes a string value",
      "The dataset loses its labels",
      "The model gains unlimited capacity",
    ],
    correctIndex: 0,
    explanation:
      "Repeated multiplication by small derivatives can shrink the backward signal through many layers. Activation choices, normalization, residual connections, and initialization help.",
  },
  {
    topic: "Preprocessing",
    difficulty: "Easy",
    question: "Why does feature standardization often help gradient-based models?",
    options: [
      "Comparable feature scales can improve optimization conditioning",
      "It guarantees perfect generalization",
      "It removes every outlier",
      "It converts classification into clustering",
    ],
    correctIndex: 0,
    explanation:
      "Large scale differences can create elongated loss contours and uneven regularization. Standardization often makes gradient updates more balanced across dimensions.",
  },
  {
    topic: "Preprocessing",
    difficulty: "Easy",
    question: "What is the usual difference between standardization and min-max normalization?",
    options: [
      "Standardization centers and scales by spread; min-max maps values to a chosen range",
      "Standardization always maps values to zero through one",
      "Min-max normalization removes all skew",
      "They are mathematically identical",
    ],
    correctIndex: 0,
    explanation:
      "Standardization commonly uses (x - mean) / standard deviation, while min-max scaling uses observed extrema. Both must be fitted on training data only.",
  },
  {
    topic: "Preprocessing",
    difficulty: "Intermediate",
    question: "Why might a log transform help a strongly right-skewed positive feature?",
    options: [
      "It compresses large values and can make multiplicative relationships easier to model",
      "It guarantees the feature becomes normally distributed",
      "It preserves zero and negative values without adjustment in every case",
      "It turns the feature into a category",
    ],
    correctIndex: 0,
    explanation:
      "A log transform can reduce scale skew and linearize some multiplicative effects. It is not universally appropriate and requires a defined treatment of non-positive values.",
  },
  {
    topic: "Preprocessing",
    difficulty: "Easy",
    question: "Why is one-hot encoding commonly used for nominal categories?",
    options: [
      "It avoids inventing an ordinal distance between category labels",
      "It always uses fewer columns than the original feature",
      "It makes every category continuous",
      "It ranks categories by importance automatically",
    ],
    correctIndex: 0,
    explanation:
      "Assigning arbitrary integers to nominal labels can suggest a false order. One-hot encoding creates indicator features, with dimensionality and unseen categories handled deliberately.",
  },
  {
    topic: "Preprocessing",
    difficulty: "Intermediate",
    question: "What is a safe way to impute missing values during cross-validation?",
    options: [
      "Fit the imputer separately on each training fold and apply it to that fold's validation data",
      "Compute imputation statistics once from the full dataset",
      "Use the test target to choose replacement values",
      "Drop all validation rows containing missing values after scoring",
    ],
    correctIndex: 0,
    explanation:
      "Preprocessing belongs inside the validation pipeline. Fitting it on all data leaks validation distribution information into training and makes estimates optimistic.",
  },
  {
    topic: "Generalization",
    difficulty: "Easy",
    question: "What is overfitting?",
    options: [
      "Learning training-specific noise or detail that does not generalize",
      "Performing poorly on both training and validation data because the model is too simple",
      "Using too few columns in a database",
      "Stopping training before one update",
    ],
    correctIndex: 0,
    explanation:
      "An overfit model has adapted too closely to its training sample, often showing a much better training score than validation or test performance.",
  },
  {
    topic: "Generalization",
    difficulty: "Intermediate",
    question: "How does the bias-variance tradeoff describe model error?",
    options: [
      "Simpler models often have higher bias and lower variance; more flexible models can reverse that balance",
      "Bias and variance are always both zero",
      "More flexibility always reduces test error",
      "Variance refers only to label class counts",
    ],
    correctIndex: 0,
    explanation:
      "High bias underfits systematic structure, while high variance makes predictions overly sensitive to the training sample. Model selection balances both for low generalization error.",
  },
  {
    topic: "Generalization",
    difficulty: "Easy",
    question: "What are the distinct roles of training, validation, and test sets?",
    options: [
      "Fit parameters on training data, choose models with validation data, and estimate final performance once on test data",
      "Fit the same model independently on all three and report the best",
      "Use test data to tune hyperparameters repeatedly",
      "Use labels only in the test set",
    ],
    correctIndex: 0,
    explanation:
      "Separating fitting, selection, and final evaluation limits adaptive overfitting to the evaluation set. Cross-validation can replace a single validation split when appropriate.",
  },
  {
    topic: "Generalization",
    difficulty: "Intermediate",
    question: "What does k-fold cross-validation estimate?",
    options: [
      "Performance across repeated train-validation partitions of the available development data",
      "The exact production error with no uncertainty",
      "Only training-set memorization",
      "The number of model parameters",
    ],
    correctIndex: 0,
    explanation:
      "Each fold serves as validation once while the remaining folds train the model. The aggregate gives a more stable selection estimate, though dependencies and time order require specialized splits.",
  },
  {
    topic: "Generalization",
    difficulty: "Intermediate",
    question: "What is data leakage?",
    options: [
      "Training uses information that would not legitimately be available when making the real prediction",
      "The model is saved to disk",
      "The training set contains more than one feature",
      "A gradient update changes parameters",
    ],
    correctIndex: 0,
    explanation:
      "Leakage includes future information, target-derived features, duplicate entities across splits, and preprocessing fitted on held-out data. It creates misleading offline performance.",
  },
  {
    topic: "Regularization",
    difficulty: "Easy",
    question: "What is the main effect of L2 regularization on model weights?",
    options: [
      "It penalizes squared weight magnitude and tends to shrink weights smoothly",
      "It forces every weight to exactly zero",
      "It adds more observations",
      "It removes the loss function",
    ],
    correctIndex: 0,
    explanation:
      "L2 adds a squared-norm penalty, discouraging large weights and often reducing variance. Coefficients usually shrink without becoming exactly zero.",
  },
  {
    topic: "Regularization",
    difficulty: "Easy",
    question: "How does L1 regularization commonly differ from L2?",
    options: [
      "L1 can drive some coefficients exactly to zero, producing sparse solutions",
      "L1 always increases every coefficient",
      "L1 can be used only with decision trees",
      "L1 has no hyperparameter controlling strength",
    ],
    correctIndex: 0,
    explanation:
      "The absolute-value L1 penalty has geometry that encourages sparse coefficients. L2 spreads shrinkage more smoothly, especially among correlated features.",
  },
  {
    topic: "Regularization",
    difficulty: "Intermediate",
    question: "What does elastic net regularization combine?",
    options: ["L1 and L2 penalties", "Dropout and early stopping", "Bagging and boosting", "Precision and recall"],
    correctIndex: 0,
    explanation:
      "Elastic net mixes L1 sparsity with L2 shrinkage. Its hyperparameters control overall strength and the relative balance between the two penalties.",
  },
  {
    topic: "Regularization",
    difficulty: "Intermediate",
    question: "How can early stopping act as regularization?",
    options: [
      "It stops optimization when held-out performance stops improving, limiting fit to training noise",
      "It removes all hidden layers before training",
      "It adds labels to unlabeled data",
      "It guarantees the global optimum",
    ],
    correctIndex: 0,
    explanation:
      "Continuing to optimize training loss can eventually fit noise. Restoring the checkpoint with the best validation metric limits effective model complexity.",
  },
  {
    topic: "Regularization",
    difficulty: "Intermediate",
    question: "What does dropout do during neural-network training?",
    options: [
      "Randomly masks a fraction of activations and rescales consistently between training and inference",
      "Deletes training examples permanently",
      "Sets the learning rate to zero",
      "Removes the output layer",
    ],
    correctIndex: 0,
    explanation:
      "Dropout injects multiplicative noise during training, discouraging brittle co-adaptation. At inference the full network is used with the framework's corresponding scaling convention.",
  },
  {
    topic: "Evaluation",
    difficulty: "Easy",
    question: "Why can accuracy be misleading on a highly imbalanced classification problem?",
    options: [
      "A model can score highly by predicting only the majority class",
      "Accuracy cannot be computed from class labels",
      "Accuracy always equals recall",
      "Imbalance makes every prediction probabilistic",
    ],
    correctIndex: 0,
    explanation:
      "When one class dominates, majority guessing can look accurate while failing on the important minority. Class-specific metrics and decision costs provide needed context.",
  },
  {
    topic: "Evaluation",
    difficulty: "Easy",
    question: "What does precision measure for a positive class?",
    options: [
      "The fraction of predicted positives that are truly positive",
      "The fraction of actual positives that were found",
      "The overall fraction of correct predictions only",
      "The average predicted probability",
    ],
    correctIndex: 0,
    explanation:
      "Precision is TP / (TP + FP), so it answers how trustworthy positive predictions are. Recall instead measures coverage of actual positives.",
  },
  {
    topic: "Evaluation",
    difficulty: "Easy",
    question: "What does recall measure for a positive class?",
    options: [
      "The fraction of actual positives that the model identifies",
      "The fraction of predicted positives that are correct",
      "The fraction of negatives predicted as negative only",
      "The model's training speed",
    ],
    correctIndex: 0,
    explanation:
      "Recall, or sensitivity, is TP / (TP + FN). It matters when missed positives carry a high cost, though threshold choice also affects false positives.",
  },
  {
    topic: "Evaluation",
    difficulty: "Intermediate",
    question: "What does the F1 score summarize?",
    options: [
      "The harmonic mean of precision and recall",
      "The arithmetic mean of accuracy and loss",
      "The variance of predicted probabilities",
      "The area under every possible learning curve",
    ],
    correctIndex: 0,
    explanation:
      "F1 balances precision and recall through their harmonic mean and becomes low if either is low. It omits true negatives and assumes equal importance for precision and recall.",
  },
  {
    topic: "Evaluation",
    difficulty: "Intermediate",
    question: "When is a precision-recall curve often more informative than an ROC curve?",
    options: [
      "When the positive class is rare and positive-prediction quality is central",
      "When there are no class labels",
      "When evaluating a regression target",
      "When the classifier outputs no ranking or score",
    ],
    correctIndex: 0,
    explanation:
      "With rare positives, many false positives can be obscured by a large count of true negatives in ROC space. Precision-recall focuses on positive detection tradeoffs.",
  },
  {
    topic: "Evaluation",
    difficulty: "Intermediate",
    question: "What does it mean for predicted probabilities to be calibrated?",
    options: [
      "Among predictions near p, the event occurs about a p fraction of the time",
      "Every prediction is either zero or one",
      "The classifier has perfect accuracy",
      "The training and test losses are identical",
    ],
    correctIndex: 0,
    explanation:
      "Calibration concerns probabilistic reliability rather than ranking or accuracy. A model can rank examples well yet systematically overstate or understate risk.",
  },
  {
    topic: "Trees and ensembles",
    difficulty: "Easy",
    question: "How does a decision tree choose a classification split?",
    options: [
      "It searches candidate splits for an impurity reduction such as Gini gain or information gain",
      "It always splits each feature at its mean",
      "It fits a single global linear coefficient",
      "It selects features alphabetically",
    ],
    correctIndex: 0,
    explanation:
      "Tree training greedily evaluates feature thresholds or category partitions to create purer child nodes. The exact criterion and constraints depend on the implementation.",
  },
  {
    topic: "Trees and ensembles",
    difficulty: "Intermediate",
    question: "Why are unconstrained decision trees prone to overfitting?",
    options: [
      "They can keep partitioning until leaves capture small, noisy subsets",
      "They have no trainable decisions",
      "They require standardized features",
      "They can model only straight lines",
    ],
    correctIndex: 0,
    explanation:
      "Deep trees have high variance and can memorize idiosyncratic training regions. Depth, leaf size, pruning, and ensembles control this flexibility.",
  },
  {
    topic: "Trees and ensembles",
    difficulty: "Easy",
    question: "What two sources of randomness are central to a random forest?",
    options: [
      "Bootstrap samples of rows and random subsets of features at splits",
      "Random target labels and random evaluation metrics",
      "Random loss functions and random test sets",
      "Random SQL queries and random seeds only",
    ],
    correctIndex: 0,
    explanation:
      "Each tree sees a bootstrap sample and considers only a random feature subset at a split. This decorrelates trees so averaging can substantially reduce variance.",
  },
  {
    topic: "Trees and ensembles",
    difficulty: "Intermediate",
    question: "What is out-of-bag evaluation in a random forest?",
    options: [
      "Scoring each training example using trees whose bootstrap samples omitted it",
      "Testing on records manually removed as outliers",
      "Evaluating without any target labels",
      "Training one tree outside the ensemble",
    ],
    correctIndex: 0,
    explanation:
      "A bootstrap sample leaves out some rows. Aggregating predictions for each row from trees that did not train on it provides an internal generalization estimate.",
  },
  {
    topic: "Trees and ensembles",
    difficulty: "Intermediate",
    question: "How does gradient boosting differ from bagging?",
    options: [
      "Boosting adds learners sequentially to correct residual errors; bagging trains learners more independently and averages them",
      "Boosting can use only linear models",
      "Bagging always has lower bias and higher variance",
      "There is no difference",
    ],
    correctIndex: 0,
    explanation:
      "Bagging primarily reduces variance through averaging diverse models. Gradient boosting builds an additive model stage by stage to reduce the current loss.",
  },
  {
    topic: "Trees and ensembles",
    difficulty: "Advanced",
    question: "Why can impurity-based tree feature importance be misleading?",
    options: [
      "It can favor high-cardinality or frequently available split features and distribute credit oddly among correlated features",
      "It is always computed on untouched test data",
      "It measures causal effect directly",
      "It cannot assign a nonzero value",
    ],
    correctIndex: 0,
    explanation:
      "Built-in split importance reflects model mechanics, not causality, and has known cardinality and correlation biases. Held-out permutation importance answers a different, often more useful question.",
  },
  {
    topic: "Classical models",
    difficulty: "Easy",
    question: "Why does k-nearest neighbors usually need feature scaling?",
    options: [
      "Large-scale features can dominate the distance calculation",
      "KNN estimates only linear coefficients",
      "Scaling chooses k automatically",
      "KNN cannot accept numeric input",
    ],
    correctIndex: 0,
    explanation:
      "KNN predictions depend directly on distances. Without scaling, a feature measured in large units can overwhelm smaller-scale but meaningful dimensions.",
  },
  {
    topic: "Classical models",
    difficulty: "Intermediate",
    question: "What is the kernel trick in a support vector machine?",
    options: [
      "Computing inner products in an implicit feature space without explicitly constructing all transformed features",
      "Randomly deleting support vectors",
      "Converting every target to a probability",
      "Replacing optimization with a decision tree",
    ],
    correctIndex: 0,
    explanation:
      "A valid kernel evaluates similarity corresponding to an implicit feature mapping, enabling nonlinear boundaries while avoiding explicit high-dimensional coordinates.",
  },
  {
    topic: "Classical models",
    difficulty: "Intermediate",
    question: "What simplifying assumption gives naive Bayes its name?",
    options: [
      "Features are conditionally independent given the class",
      "All classes have identical prior probability",
      "Every feature follows a uniform distribution",
      "The target is independent of every feature",
    ],
    correctIndex: 0,
    explanation:
      "Naive Bayes factors the class-conditional likelihood by assuming conditional feature independence. The assumption is often false, yet the classifier can still work well.",
  },
  {
    topic: "Unsupervised learning",
    difficulty: "Easy",
    question: "What objective does k-means clustering minimize?",
    options: [
      "The within-cluster sum of squared distances to cluster centroids",
      "Classification cross-entropy against known labels",
      "The number of features",
      "The maximum distance between every pair of data points",
    ],
    correctIndex: 0,
    explanation:
      "K-means alternates assigning points to nearest centroids and recomputing centroids to reduce within-cluster squared Euclidean distance. Initialization can affect the local solution.",
  },
  {
    topic: "Unsupervised learning",
    difficulty: "Intermediate",
    question: "What does the first principal component in PCA represent?",
    options: [
      "The unit direction capturing the greatest variance in the centered data",
      "The original feature with the largest name",
      "The class label with the most examples",
      "The nonlinear boundary with perfect accuracy",
    ],
    correctIndex: 0,
    explanation:
      "PCA finds orthogonal directions of decreasing variance, with the first maximizing projected variance. Scaling matters when feature units differ.",
  },
  {
    topic: "Unsupervised learning",
    difficulty: "Intermediate",
    question: "What is a limitation of using PCA solely because it retains high variance?",
    options: [
      "High-variance directions are not guaranteed to be most predictive of the target",
      "PCA cannot reduce dimensionality",
      "PCA always uses labels and therefore leaks them",
      "Principal components are never orthogonal",
    ],
    correctIndex: 0,
    explanation:
      "PCA is unsupervised and ignores target relevance. A low-variance direction can still carry important predictive or causal signal.",
  },
  {
    topic: "Neural networks",
    difficulty: "Easy",
    question: "What does backpropagation compute?",
    options: [
      "Loss gradients with respect to parameters by applying the chain rule through the computation graph",
      "A random set of model weights",
      "The final train-test split",
      "Only the forward predictions",
    ],
    correctIndex: 0,
    explanation:
      "Backpropagation efficiently propagates derivative information backward through composed operations. An optimizer then uses those gradients to update parameters.",
  },
  {
    topic: "Neural networks",
    difficulty: "Easy",
    question: "Why are nonlinear activation functions needed between neural-network layers?",
    options: [
      "Without them, stacked linear layers collapse to one linear transformation",
      "They guarantee every gradient is one",
      "They remove all trainable parameters",
      "They make input data unnecessary",
    ],
    correctIndex: 0,
    explanation:
      "Composing affine transformations without nonlinearities remains affine, regardless of depth. Activations let networks represent nonlinear functions.",
  },
  {
    topic: "Neural networks",
    difficulty: "Intermediate",
    question: "What problem do residual connections help address in deep networks?",
    options: [
      "They provide short paths for signals and gradients through many layers",
      "They remove the need for a loss function",
      "They make every layer have zero parameters",
      "They convert supervised learning into k-means",
    ],
    correctIndex: 0,
    explanation:
      "A residual block learns a change around an identity path. The shortcut improves information and gradient flow and makes very deep optimization more practical.",
  },
  {
    topic: "Neural networks",
    difficulty: "Intermediate",
    question: "How does layer normalization differ conceptually from batch normalization?",
    options: [
      "Layer normalization normalizes across features within an example; batch normalization uses batch statistics for each feature",
      "Layer normalization requires larger batches than batch normalization",
      "Batch normalization has no learned scale or shift",
      "They are always identical for every tensor",
    ],
    correctIndex: 0,
    explanation:
      "Layer norm does not depend on other batch examples, which suits variable sequence workloads. Batch norm uses training-batch statistics and tracked inference behavior.",
  },
  {
    topic: "Transformers",
    difficulty: "Easy",
    question: "In self-attention, what roles do queries, keys, and values play?",
    options: [
      "Query-key similarity creates attention weights used to combine the values",
      "Queries are labels, keys are losses, and values are gradients",
      "Keys choose the optimizer and values choose the batch size",
      "All three are fixed one-hot vectors with identical roles",
    ],
    correctIndex: 0,
    explanation:
      "Each token projects to queries, keys, and values. A query scores keys to decide where to attend, and normalized scores form a weighted mixture of value vectors.",
  },
  {
    topic: "Transformers",
    difficulty: "Intermediate",
    question: "Why is the query-key dot product scaled by the square root of key dimension in standard attention?",
    options: [
      "To keep logits from growing too large and pushing softmax into saturated regions",
      "To make sequence length always equal key dimension",
      "To remove the need for values",
      "To guarantee sparse attention",
    ],
    correctIndex: 0,
    explanation:
      "Dot-product variance grows with vector dimension. Dividing by sqrt(d_k) keeps score magnitudes better conditioned for softmax and gradient flow.",
  },
  {
    topic: "Transformers",
    difficulty: "Intermediate",
    question: "What is the purpose of multi-head attention?",
    options: [
      "To let separate learned projections attend to different relationships or representation subspaces",
      "To run the exact same attention result repeatedly with no learned differences",
      "To eliminate all feed-forward layers",
      "To force every token to attend only to itself",
    ],
    correctIndex: 0,
    explanation:
      "Multiple heads use different projections and can capture complementary patterns. Their outputs are combined into the layer representation.",
  },
  {
    topic: "Transformers",
    difficulty: "Easy",
    question: "Why do transformers need positional information?",
    options: [
      "Self-attention alone has no inherent notion of token order",
      "Token embeddings already encode every possible sequence position permanently",
      "Positions replace token identities",
      "Positional information is used only to choose the optimizer",
    ],
    correctIndex: 0,
    explanation:
      "Attention over a set of token representations is otherwise permutation-equivariant. Positional encodings or embeddings inject ordering and distance information.",
  },
  {
    topic: "Transformers",
    difficulty: "Intermediate",
    question: "What does a causal attention mask enforce in an autoregressive transformer?",
    options: [
      "A position cannot attend to future positions when predicting the next token",
      "Every position attends equally to every future token",
      "Padding tokens become target labels",
      "The vocabulary is sorted alphabetically",
    ],
    correctIndex: 0,
    explanation:
      "Causal masking prevents information leakage from later tokens into earlier predictions, matching left-to-right generation at inference time.",
  },
  {
    topic: "Transformers",
    difficulty: "Intermediate",
    question: "What is the main computational bottleneck of full self-attention for long sequences?",
    options: [
      "Its attention matrix grows quadratically with sequence length",
      "It has no matrix multiplications",
      "Its parameter count always grows with every input token",
      "It cannot run on parallel hardware",
    ],
    correctIndex: 0,
    explanation:
      "Pairwise token attention produces an n by n score structure, creating quadratic time and memory pressure in sequence length for standard full attention.",
  },
  {
    topic: "Production ML",
    difficulty: "Intermediate",
    question: "What is concept drift?",
    options: [
      "The relationship between inputs and target changes over time",
      "A model file moves to another folder",
      "The training loss decreases",
      "A feature is standardized",
    ],
    correctIndex: 0,
    explanation:
      "Concept drift changes P(y|x), so a previously valid decision function can degrade. Data drift changes input distribution and may or may not imply concept drift.",
  },
  {
    topic: "Production ML",
    difficulty: "Intermediate",
    question: "Why should production monitoring include input data as well as model accuracy?",
    options: [
      "Labels may arrive late, while schema, missingness, and distribution shifts can provide earlier warnings",
      "Input monitoring guarantees that labels are correct",
      "Accuracy can always be measured instantly in production",
      "Models never fail when input distributions are stable",
    ],
    correctIndex: 0,
    explanation:
      "Operational and feature checks can detect broken pipelines or changed populations before ground truth matures. They complement, not replace, outcome-based monitoring.",
  },
  {
    topic: "Production ML",
    difficulty: "Advanced",
    question: "Why is an offline metric improvement not enough to guarantee product impact?",
    options: [
      "The metric may not capture user behavior, system interactions, latency, or the true decision cost",
      "Offline evaluation never uses data",
      "Online experiments cannot measure outcomes",
      "Every offline metric is mathematically invalid",
    ],
    correctIndex: 0,
    explanation:
      "A model lives inside a product and policy. Online tests and guardrails can reveal feedback loops, behavior changes, latency costs, and business outcomes absent from a static dataset.",
  },
  {
    topic: "Experiment design",
    difficulty: "Intermediate",
    question: "What is a hyperparameter rather than a learned parameter?",
    options: ["The regularization strength selected during model development", "A fitted linear-regression coefficient", "A learned neural-network bias", "A decision-tree split chosen by training"],
    correctIndex: 0,
    explanation:
      "Hyperparameters configure training or model capacity and are selected outside the ordinary parameter-fitting loop. Weights, biases, and fitted splits are learned parameters.",
  },
  {
    topic: "Experiment design",
    difficulty: "Intermediate",
    question: "Why should random seeds not be treated as a substitute for repeated evaluation?",
    options: [
      "One seed can hide variance from initialization, sampling, and splitting",
      "Seeds make experiments impossible to reproduce",
      "Every seed produces exactly the same result",
      "Repeated evaluation always causes data leakage",
    ],
    correctIndex: 0,
    explanation:
      "A fixed seed supports reproducibility but gives one realization of stochastic training and sampling. Multiple seeds or confidence intervals reveal result variability.",
  },
  {
    topic: "Experiment design",
    difficulty: "Advanced",
    question: "Why is a time-based split often necessary for forecasting or future-event prediction?",
    options: [
      "It preserves temporal causality and tests on observations later than training data",
      "It guarantees all seasons appear equally in every split",
      "It allows future features to train past predictions",
      "It always creates balanced target classes",
    ],
    correctIndex: 0,
    explanation:
      "Random splitting can leak future regimes or repeated entities into training. A chronological split better simulates deployment, though rolling backtests are often needed for robustness.",
  },
]);
