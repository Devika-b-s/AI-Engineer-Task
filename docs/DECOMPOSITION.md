# Decomposition (fill this in BEFORE writing code)

Commit this file on its own before any code. Write plainly. If you use AI to help you think, that's fine, but the final text must be what *you* understand. We will ask you about it.

## 1. The problem in my own words

In 3-5 sentences, say what you are being asked to build. Don't use a term you couldn't explain to a friend.

I need to build a system that reads a WhatsApp group chat and helps people understand the current status.The chat contains different people discussing tasks, assigning responsibilities, changing decisions, and updating deadlines over time.My system should understand these conversations and answer questions in English or Hinglish using the latest available information. 

## 2. What I noticed in the data

Read `data/team_chat.txt` completely. List **at least 5 specific things** in the chat that would make it hard for a system to answer questions correctly. For each, quote the message (with date and time) and explain why it's hard.

| # | What I noticed (quote + timestamp) | Why it makes answering hard |
|---|---|---|
| 1 |05/10/26, 8:02 PM – Aarav: "Rohan - auth (login/signup)" 

24/10/26, 11:25 PM – Kabir: "arre theek hai, auth bhi le leta hoon."|

The person responsible for authentication changes from Rohan to Kabir. The system must identify the latest assignment instead of returning the original owner. |

| 2 | 20/10/26, 8:16 PM – Aarav: "agreed. final decision: no Razorpay, UPI QR manual" 

 02/11/26, 8:49 PM – Aarav: "haan. Razorpay test mode final. QR wala scrap." |

 The payment decision is reversed. The system must understand that the latest decision replaces the earlier one. |
| 3 |12/10/26, 7:30 PM – Meera: "Demo day 4 Dec so report 1 Dec" 

 05/11/26, 6:10 PM – Aarav: "ab 27 Nov (Friday)" 

 09/11/26, 5:30 PM – Priya: "Demo day 26 Nov (Thursday), 27 nahi. Correction." |
 
 The deadline changes multiple times. The system must consider the latest correction and not use an outdated date. |
| 4 |19/10/26, 6:16 PM – Kabir: "chat main kar lunga. search koi aur le lo please" 

 10/11/26, 9:15 PM – Priya: "great. search ka kya? abhi bhi koi nahi le raha"|
 
 Search functionality has no confirmed owner. The system must distinguish between a confirmed and unconfirmed assignment.|
| 5 |06/11/26, 11:06 PM – Rohan: "tests kal raat tak kar dunga" 

 07/11/26, 11:50 PM – Rohan: "sorry yaar, tests nahi ho paye. kal pakka" 

 09/11/26, 5:40 PM – Rohan: "tests ab bhi pending hain, I'll do by this Sunday"|
 
 A person may promise to complete a task without actually completing it. The system should track confirmed completion rather than treating promises as completed work.|

## 3. The simplest thing that could work, and how it would fail

Describe the dumbest reasonable approach (maybe 3 lines). Then write **3 questions about this chat that it would get wrong**, and say exactly why.

1.Who is currently responsible for authentication?
A keyword search might return Rohan because his name appears in the original assignment.But Kabir took over authentication on 24 October and confirmed completion on 10 November.The correct answer is Kabir.

2.What is the final payment decision?
A simple search might find the 20 October decision saying Razorpay was cancelled and switched to QR  with manual confirm.However, on 2 November the team changed its decision and selected Razorpay test mode.The correct answer is Razorpay test mode, and the UPI QR approach was cancelled.

3.When is the project demo?
The search might return 4 December or 27 November.
However, Priya corrected the date on 9 November because the college notice contained a typo.The latest confirmed date is 26 November 2026.

## 4. Break it into sub-problems

List the smaller problems the whole task is made of. For each one write:

- **Input:** what goes in
- **Output:** what comes out
- **How I'll know it's working:** a check you can actually run

Include a diagram of how the pieces connect. ASCII art or a photo of a hand-drawn sketch is fine.

Chat file reading and parsing

Input: A WhatsApp exported .txt file.
Output: Individual messages containing timestamp, sender and message text.
How I'll know it's working: I will run the parser on team_chat.txt and check whether it extracts the messages, timestamps and sender names correctly. I will also check messages containing media placeholders and multiline text.

Understanding and extracting information

Input: Parsed messages.
Output: Structured information about tasks, people, decisions, deadlines and status updates.
How I'll know it's working: I will check specific examples, such as identifying Kabir as the new authentication owner and identifying the Razorpay test-mode decision.

Tracking task ownership and completion

Input: Messages containing task assignments, reassignment and progress updates.
Output: A list of tasks, their latest known owners and completion status.
How I'll know it's working: I will check that authentication is marked completed under Kabir, tests remain pending under Rohan, and search is shown as unassigned.

Question understanding and answering

Input: A question in English or Hinglish and the extracted project information.
Output: An understandable answer based on the available chat information.
How I'll know it's working: I will ask questions about task ownership, project status, deadlines and decisions in both English and Hinglish and compare the answers with manually verified results.

Evidence retrieval

Input: An answer and the messages supporting it.
Output: Evidence containing the original timestamp, sender and message.
How I'll know it's working: Every answer that makes a factual claim should show the message or messages supporting that claim. I will verify that the evidence actually supports the answer.

Handling missing information

Input: Questions whose answers are not available in the chat.
Output: A clear response saying that the chat doesn't say or does not provide enough information.
How I'll know it's working: I will ask questions about information that is missing, such as the actual receipt amount or whether the Render deployment was successfully completed.

WhatsApp Chat -> File Parser -> Parsed Messages
                                      |
                                      v
                           Information Extraction
                                     |
    ----------------------------------------
   |                    |                  |
   v                    v                  v
Tasks                 Decisions         Deadlines
   |                    |                  |
   -----------------------------------------
                        |
                        v
            -------------------------
            |                       |
            v                       v
    Question Answering      Project Status
                 

## 5. What I don't know yet

List the things you'd need to learn or find out. For each, write how you plan to find out (docs, experiment, ask an AI and then verify it, etc.).

1.WhatsApp export format and different timestamp formats - Study the sample file and test Python regular expressions on different message formats.

2.Extracting tasks, decisions and deadlines from informal messages - Start with Python rules and patterns, then explore NLP or LLM-based extraction if needed.

3.Understanding English and Hinglish messages - Study common phrases in the chat and test how the extraction logic handles them.

4.Answering questions with supporting evidence - Learn how to retrieve relevant messages and connect them to answers.

5.Tracking changes and identifying the latest information - Design a structured representation of tasks and decisions and test it against the chronological messages.

## 6. Build order

What is the smallest end-to-end slice you'll build first (even if it's bad)? What comes second? Why that order?

Step 1: Build a basic chat parser
Every other part of the system depends on correctly reading the chat.

Step 2: Extract basic project information
The system needs structured information before it can answer meaningful questions

Step 3: Build a basic end-to-end question-answering system
This gives me the smallest working version of the complete application.

Step 4: Add chronological state tracking
The main difficulty in this assignment is finding the current information instead of returning outdated information.

Step 5: Add task status and unassigned-task detection
This is necessary for answering project-status questions correctly.

Step 6: Improve English and Hinglish question handling
The assignment explicitly requires both English and Hinglish support.

Step 7: Add the complete project-status report
This provides an overall view of the project without requiring users to ask individual questions.

## 7. Where I'll use AI, and where I won't

Be specific. For example, "I'll let AI write the file parser, but I'll design the data model myself because ___."

I will use
1.To help understand unfamiliar NLP concepts
2.To explore ways of extracting information from English and Hinglish messages.
3.To review my code and suggest possible improvements.
4.To review my code and suggest possible improvements.

I won't use
1.I will design the overall system structure and decide how its components connect.
2.I will verify the actual task owners, deadlines and decisions using the original chat messages.
3.I will ensure that answers have supporting evidence.
4.I will maintain the task and decision history so that earlier information is not incorrectly treated as current.s