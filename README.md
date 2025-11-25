# Election Management System – Python Tkinter + MySQL

A desktop application for conducting **secure and accurate digital elections**.  
It supports **three voting methods** used in real-world democracy and ensures **voter authentication, no duplicate voting, and automatic winner calculation**.

---

## Voting Modes Supported
| Mode | Description |
|------|-------------|
| FPTP (First Past The Post) | Each voter selects one candidate → most votes wins |
| Approval Voting | Voter can approve multiple candidates → most approvals win |
| IRV (Instant Runoff / Ranked Choice) | Lowest candidate eliminated each round until someone achieves 50%+ majority |

---

## Core Features
- Admin login with password stored in DB
- Voter validation (name + voter number)
- Prevents duplicate voting
- GUI built with Tkinter (fullscreen support)
- Results instantly computed and displayed
- Winner stored permanently in database
- Scalable for any number of candidates

---

## Tech Stack
| Component | Technology |
|----------|-------------|
| Programming Language | Python |
| GUI Framework | Tkinter |
| Database | MySQL |
| DB Connector | PyMySQL |

---

## Database Schema — COMPLETE

Database name: **`election`**

### - `admin`
| Column | Type | Notes |
|--------|------|-------|
| password | VARCHAR(255) | Stores admin login password |

### - `voters`
| Column | Type | Notes |
|--------|------|-------|
| name | VARCHAR(255) | Voter name |
| voter_number | INT | Unique voter ID |
| voted | TINYINT(1) | 0 = not voted, 1 = voted |

### - `candidates`
| Column | Type | Notes |
|--------|------|-------|
| candidate_id | INT | PK, AUTO_INCREMENT |
| candidate_name | VARCHAR(255) | Candidate name |

### - `votes_fptp`
| Column | Type | Notes |
|--------|------|-------|
| candidate_name | VARCHAR(255) | Candidate voted |
| count | INT | Total votes received |

### - `votes_approval`
| Column | Type | Notes |
|--------|------|-------|
| candidate_name | VARCHAR(255) | Candidate approved |
| approvals | INT | Total approval ticks |

### - `votes_irv`
| Column | Type | Notes |
|--------|------|-------|
| voter_name | VARCHAR(255) | Voter who cast ranked vote |
| rank_1 | VARCHAR(255) | 1st preference |
| rank_2 | VARCHAR(255) | 2nd preference |
| rank_3 | VARCHAR(255) | 3rd preference |
> (Supports additional columns if more candidates exist)

### - `winners`
| Column | Type | Notes |
|--------|------|-------|
| election_id | INT | PK |
| winner | VARCHAR(255) | Final winner name |

---

## Entity–Relationship Diagram (ASCII)
                ┌──────────────┐
                │    admin     │
                ├──────────────┤
                │  password    │
                └──────────────┘
                        │
                        │ controls
                        ▼
                ┌──────────────┐
                │    voters    │
                ├──────────────┤
                │ name         │
                │ voter_number │
                │ voted        │
                └──────────────┘
                        │
                        │ can vote for
                        ▼
                ┌──────────────┐
                │  candidates  │
                ├──────────────┤
                │ candidate_name │
                └──────────────┘
                        │
                        │ winner calculated from voting
                        ▼
                ┌──────────────┐
                │   winners    │
                ├──────────────┤
                │ election_id  │
                │ winner       │
                └──────────────┘

## Setup Instructions
  pip install pymysql
  python main.py
## Winner decision logic
| Voting Mode | Voting Methodology | Decision Rule |
|-------------|---------------------|--------------|
| FPTP (First Past The Post) | Each voter selects one candidate | Candidate with the highest vote count wins |
| Approval Voting | A voter can approve one or more candidates | Candidate with the highest number of approvals wins |
| IRV (Instant Runoff / Ranked Choice) | Voters rank candidates in order of preference | If no candidate gets 50%+ of first-choice votes, the lowest candidate is eliminated and votes are transferred until one candidate passes 50% |
## Suggested Repository Folder Layout
    Election-Management-System/
    │-- output_screenshots
    │-- README.md
    │-- election.sql
    │-- main_program.py
## Additional Notes
  - Admin selects voting mode before voting begins
  - Voters cannot vote twice — validated using name + voter number
  - Winner is automatically stored inside the database
## Future Enhancements
  - OTP / QR-based voter verification.
  - Export result to PDF.
  - Web deployment & cloud database.
  - Multi-election history dashboard.
