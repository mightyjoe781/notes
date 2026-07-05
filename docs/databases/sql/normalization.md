---
title: Database Normalization (1NF, 2NF, 3NF, BCNF)
description: Walks a messy student-courses table through 1NF, 2NF, 3NF, and BCNF, explaining the functional-dependency violation each normal form removes.
tags:
  - concept
---

# Database Normalization (1NF, 2NF, 3NF, BCNF)

Normalization is the process of organizing columns and tables to reduce data redundancy and avoid anomalies (insert, update, delete anomalies). Each normal form builds on the previous one - you can't be in 3NF without first being in 2NF and 1NF.

We'll use one running example - a messy `STUDENT_COURSES` table - and fix it one normal form at a time.

## The Problem Table

| StudentID | StudentName | CourseID | CourseName | Grades | InstructorID | InstructorName | InstructorPhone |
| --------- | ----------- | -------- | ---------- | ------ | ------------ | -------------- | --------------- |
| 1         | Alice       | C1       | DBMS       | A, B+  | I1           | Dr. Rao        | 9999999999      |
| 1         | Alice       | C2       | OS         | A      | I2           | Dr. Mehta      | 8888888888      |
| 2         | Bob         | C1       | DBMS       | B      | I1           | Dr. Rao        | 9999999999      |

This single table has every classical anomaly - repeated instructor info, multi-valued grades, redundant course names. Let's fix it.

## 1NF - First Normal Form

**Rule:** Every column must hold a single atomic value. No repeating groups, no comma-separated lists, no arrays in a cell.

**Violation:** Alice's `Grades = "A, B+"` crams two values into one cell.

**Fix:** One row per enrollment, so each row is uniquely identified by `(StudentID, CourseID)`.

| StudentID | StudentName | CourseID | CourseName | Grade | InstructorID | InstructorName | InstructorPhone |
|-----------|-------------|----------|------------|-------|--------------|----------------|-----------------|
| 1         | Alice       | C1       | DBMS       | A     | I1           | Dr. Rao        | 9999999999      |
| 1         | Alice       | C1       | DBMS       | B+    | I1           | Dr. Rao        | 9999999999      |
| 1         | Alice       | C2       | OS         | A     | I2           | Dr. Mehta      | 8888888888      |
| 2         | Bob         | C1       | DBMS       | B     | I1           | Dr. Rao        | 9999999999      |

We're in 1NF now - no multi-value cells. But `StudentName` only depends on `StudentID`, not on the full `(StudentID, CourseID)` key. That's the 2NF problem.

**Test question:** "Does any cell hold more than one value?"

## 2NF - Second Normal Form

**Rule:** Must be in 1NF, and every non-key column must depend on the *entire* composite primary key, not just part of it.

**Violation:** `StudentName` depends only on `StudentID`. `CourseName`, `InstructorID`, `InstructorName`, `InstructorPhone` depend only on `CourseID`. Neither depends on the full `(StudentID, CourseID)` key - these are **partial dependencies**.

**Fix:** Split into separate tables, one per entity that has its own identity.

`STUDENTS`

| StudentID | StudentName |
|-----------|-------------|
| 1         | Alice       |
| 2         | Bob         |

`COURSES`

| CourseID | CourseName | InstructorID | InstructorName | InstructorPhone |
|----------|------------|--------------|----------------|-----------------|
| C1       | DBMS       | I1           | Dr. Rao        | 9999999999      |
| C2       | OS         | I2           | Dr. Mehta      | 8888888888      |

`ENROLLMENTS`

| StudentID | CourseID | Grade |
|-----------|----------|-------|
| 1         | C1       | A     |
| 1         | C1       | B+    |
| 1         | C2       | A     |
| 2         | C1       | B     |

Better - but in `COURSES`, `InstructorPhone` doesn't depend on `CourseID` directly. It depends on `InstructorID`, which itself depends on `CourseID`. That non-key -> non-key chain is what 3NF removes.

**Test question:** "Does any non-key column depend on only part of the composite key?"

## 3NF - Third Normal Form

**Rule:** Must be in 2NF, and no non-key column should depend on another non-key column (no **transitive dependencies**).

**Violation:** In `COURSES`, `CourseID -> InstructorID -> InstructorName, InstructorPhone`. The instructor attributes depend on `InstructorID`, not directly on `CourseID`.

**Fix:** Pull instructors into their own table.

`COURSES`

| CourseID | CourseName | InstructorID |
|----------|------------|--------------|
| C1       | DBMS       | I1           |
| C2       | OS         | I2           |

`INSTRUCTORS`

| InstructorID | InstructorName | InstructorPhone |
|--------------|----------------|-----------------|
| I1           | Dr. Rao        | 9999999999      |
| I2           | Dr. Mehta      | 8888888888      |

**Test question:** "Does any non-key column depend on another non-key column?"

## BCNF - Boyce-Codd Normal Form

**Rule:** For every functional dependency `X -> Y`, `X` must be a superkey (i.e. `X` must uniquely identify a whole row). No exceptions.

3NF leaves one loophole: a non-superkey is allowed to determine a *prime attribute* (an attribute that is part of some candidate key). BCNF closes that loophole.

**Where 3NF isn't enough - extended example:** Suppose each course can have multiple instructors, each instructor teaches only one course, and each student is assigned exactly one instructor per course. This produces a `STUDENT_INSTRUCTOR` table with overlapping candidate keys `(StudentID, CourseID)` and `(StudentID, InstructorID)`.

Here `InstructorID -> CourseID` holds. This passes 3NF because `CourseID` is a *prime attribute* (part of the candidate key `(StudentID, CourseID)`). But it fails BCNF because `InstructorID` alone is not a superkey - it doesn't determine the whole row (it doesn't determine `StudentID`).

**Fix:** Decompose so the determinant `InstructorID` becomes a key in its own table (e.g. an `INSTRUCTOR_COURSE` table mapping `InstructorID -> CourseID`, separate from the student assignment).

**Test question:** "Does every determinant on the left side of a functional dependency happen to be a superkey?"

## 3NF vs BCNF - the key distinction

Both eliminate transitive dependencies, but they differ on one edge case:

- **3NF allows:** `non-superkey -> prime attribute`
- **BCNF forbids it entirely** - every determinant must be a superkey, no exceptions

**Rule of thumb:** If a table has only one candidate key, 3NF and BCNF are equivalent - the edge case can't arise. The distinction only shows up with multiple overlapping candidate keys.

## Summary

| Form | Eliminates                  | Test question                                                          |
|------|-----------------------------|------------------------------------------------------------------------|
| 1NF  | Multi-value / non-atomic cells | Does any cell hold more than one value?                            |
| 2NF  | Partial dependencies        | Does any non-key column depend on only part of the composite key?      |
| 3NF  | Transitive dependencies     | Does any non-key column depend on another non-key column?              |
| BCNF | Edge cases left by 3NF      | Does every determinant happen to be a superkey?                        |

For interviews, 3NF is the core expectation - you'll often be given a denormalized table and asked to decompose it through 1NF -> 2NF -> 3NF. BCNF tends to show up in senior rounds, and only matters when a table has multiple overlapping candidate keys.

## See Also
- [Data Warehouse Schema Design](data_warehousing.md)
- [Data Modelling](../../sd/topics/database/data_modelling.md)
