All the data are for CFA Level 1.

## Content

The data are split into 2 parts: course material and questions/answers.

The course material contains : 
* Standards of Practice Handbook and related files
* 2015 Study Notebooks and QuickSheet
* Mock & Sample exam Q&A
* Practice exams Q&A

### Naming convention
For the folders, the prefix **material** indicates that it contains course material, whereas **qa** indicates that it contains Questions/Answers.

### Data type

Data may exist in different formats: pdf, xml, txt, jpg.
Some data may exist in some formats and not in others, and a conversion may be needed in order to standardise the formats and facilite processing (cf. Methodology).

### Note on the CFA questions

* All the questions are *simulated questions* and do not correspond to real exam questions.

* In real CFA exams, the questions follow the order of the topics, but all topics may not always appear, and the number of questions is not always the same.

* In mock and practice exams, the number of questions per topic may be explicitly given at the beginning of the file.

* The questions in *practice exams* are ordered and the correspondance between questions and topics are explicitly given at the beginning of the book. In mock exams, the correspondance is sometimes given.

* The *mock exams 2008-2013* (xml) are cleaned and formatted data.

### Description of folders

#### material_handbook

Contains:

* [The Code of Ethics & Standards of Professional Conduct](https://www.cfainstitute.org/ethics/codes/ethics/Pages/index.aspx) (pdf)

The Code of Ethics and Standards of Professional Conduct ("Code and Standards") are the ethical benchmark for investment professionals around the globe, regardless of job title, cultural differences, or local laws.

Students are required to know the Standards of Professional Conduct (e.g. What does I.A in the Standards of Professional Conduct correspond to ?)

* The Standards of Practice Handbook 2014 (pdf)

The Standards of Practice Handbook grounds the concepts covered in the Code and Standards for practical use. You can use this handbook for guidance on how to navigate ethical dilemmas you might face in your daily professional life.
It contains a more detailed description of the concepts.

* Errata of The Standards of Practice Handbook 2014 (pdf)

#### material_curriculum

Contains:

* Program Curriculum 2017 (pdf and txt)

Contains all the course material, and is organized into 18 study sessions.
Each study session includes assigned readings, learning outcome statements (LOS), and problem sets.

* Errata of the Program Curriculum 2017 (pdf)

* LOS Command Words (pdf)

Learning Outcome Statements (**LOS**) : Describes what the candidates should be able to know/do. It describes the specific knowledge, skills, and abilities that the candidates should be able to apply after completing a reading. LOS use command words such as “demonstrate,” “formulate,” or “evaluate” to indicate how much you should know about a given topic.

#### material_notebooks_and_quicksheets/2015

Contains: 

* The 2015 Study Notebooks 1-5 (pdf, and 1-2 also in xml)

Contains a resume of the Program Curriculum according to the key Learning Outcome Statements (LOS).
The Notebooks are often used by the candidates instead of the Program Curriculum, since more condensed. 
The xml is obtained after OCR, and not parsed.

* The 2015 QuickSheet (pdf and xml)

A summarize of the key formulas, definitions and concepts.
The xml is obtained after OCR, and not parsed.

#### material_notebooks_and_quicksheets/study_sessions

Contains:

* Study Sessions Level 1 2017 (pdf and txt)

There are 18 study sessions. The *combined* file contains the same information than the 18 split files.
Each study session contains reading assignment source references and LOS for the readings.

#### qa_mock_exams

There are 120 questions in each session (240 questions for each year).

Contains: 

* Mock Exam questions 2008-2013 (pdf and xml)
The xml is obtained after OCR, and parsed.

* Mock Exam questions 2014-2017 (pdf and jpg)
For 2016, the questions and answers are in separated files.
For other years, the questions and answers are included in the same file.

#### qa_practice_exams

Contains: 

* Practice Exam questions 2008-2011, 2014-2015 (pdf, xml for 2011 and 2014)

For 2008, 2010 and 2015, there is only the Volume 1.
For other years, both volumes are in the dataset.

#### qa_sample_exams

Contains: 

* Sample Exam questions 2010-2014 (pdf, xml and xhtml)

> **Note**

* The questions of [2011_CFA_Level_1_Sample_Exams_v1_2 are all included in [2010-2013_CFA_Level_1_Sample_exams] (section 2010 CFA Level 1 Sample Exam). 
However the answers in [2011_CFA_Level_1_Sample_Exams_v1_2] provides a bit more information, in particular they include a reference to the textbooks.

## Indications about data processing

* It is possible to start by exploring and cleaning the dataset. The questions in *mock exam 2008-2013* are cleaned and formatted, and could be used as a starting point.

* For .pdf and .jpg data, it is possible to extract the text using Google Vision API (OCR) or Microsoft Azure API Vision (OCR). For Google Cloud, a credit of 300$ is given at subscription.

## Suggested approaches

* General idea : Classify questions according to the type of answer asked/type of resolution/topic of the question, in order to reduce the information research scope; then create a resolver for each class of question, starting by the *easiest* types of question.

* In some problems, the formulation may contain a lot of information, not all useful for the resolution. It is possible to start by looking at the answers and the question (usually the last sentence in the problem formulation) first in order to get an idea of what is asked and limit the scope of research, and potentially to assign different weights to different parts of the problem formulation.

* Some questions in the Ethical part - the situational ones - may be quite difficult to tackle, thus it is advised to start by looking at different types of questions that may exist, and not start by the most difficult ones.