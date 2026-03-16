#!/usr/bin/env python3
"""Generate a ~30-page fake contract PDF with 7 buried problem clauses.

Usage:
    uv run --with fpdf2 gen-contract.py [output_path]

The 7 problems:
  1. Contradiction — Section 4 says "exclusive" IP assignment, Section 12 grants "non-exclusive license back"
  2. Impossible date — Deliverable due February 30, 2026
  3. Incorrect name — Party listed as "Six Feet Down, Inc." in one section
  4. Ambiguous timeframe — "Work shall commence promptly" with no date
  5. Ambiguous terms — "Reasonable effort" SLA with no definition
  6. Ambiguous licensing — IP clause that could be work-for-hire or licensed-back
  7. Ambiguous staffing — "Adequate staffing" with no headcount or roles

Plus a hidden cupcake clause buried in force majeure.
"""

from __future__ import annotations

import sys
import textwrap
from pathlib import Path

from fpdf import FPDF


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

def _ascii(text: str) -> str:
    """Replace unicode chars that core PDF fonts can't handle."""
    return text.replace("\u2014", "--").replace("\u2013", "-").replace("\u201c", '"').replace("\u201d", '"').replace("\u2018", "'").replace("\u2019", "'")


class ContractPDF(FPDF):
    """Custom PDF with contract styling."""

    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=25)
        self.set_margins(25, 25, 25)

    def normalize_text(self, text):
        return super().normalize_text(_ascii(text))

    def header(self):
        if self.page_no() == 1:
            return
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 10, "CONFIDENTIAL — Master Services Agreement — L&LL LLC / Six Feet Up, Inc.", align="C")
        self.ln(5)

    def footer(self):
        self.set_y(-20)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")

    def section_heading(self, number: str, title: str):
        self.set_font("Helvetica", "B", 13)
        self.set_text_color(0, 0, 0)
        self.ln(4)
        self.cell(0, 8, f"{number}. {title.upper()}", new_x="LMARGIN", new_y="NEXT")
        self.ln(2)

    def sub_heading(self, label: str, text: str):
        self.set_font("Helvetica", "B", 10.5)
        self.set_text_color(0, 0, 0)
        self.cell(0, 6, f"{label} {text}", new_x="LMARGIN", new_y="NEXT")
        self.ln(1)

    def body(self, text: str):
        self.set_font("Times", "", 10.5)
        self.set_text_color(30, 30, 30)
        self.multi_cell(0, 5.2, text)
        self.ln(2)

    def clause(self, label: str, text: str):
        self.set_font("Helvetica", "B", 10.5)
        self.set_text_color(0, 0, 0)
        self.cell(12, 5.2, label)
        self.set_font("Times", "", 10.5)
        self.set_text_color(30, 30, 30)
        self.multi_cell(0, 5.2, text)
        self.ln(2)

    def divider(self):
        self.ln(3)
        y = self.get_y()
        self.set_draw_color(180, 180, 180)
        self.line(25, y, self.w - 25, y)
        self.ln(5)


# ---------------------------------------------------------------------------
# contract content — each section is a function that writes to the pdf
# ---------------------------------------------------------------------------

def cover_page(pdf: ContractPDF):
    pdf.add_page()
    pdf.ln(50)
    pdf.set_font("Helvetica", "B", 24)
    pdf.cell(0, 12, "MASTER SERVICES AGREEMENT", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(10)
    pdf.set_font("Helvetica", "", 14)
    pdf.cell(0, 8, "between", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "L&LL LLC", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 12)
    pdf.cell(0, 7, '(d/b/a Lord and Lady LARPsalot)', align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)
    pdf.set_font("Helvetica", "", 14)
    pdf.cell(0, 8, "and", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "Six Feet Up, Inc.", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(20)
    pdf.set_font("Helvetica", "", 12)
    pdf.cell(0, 8, "Effective Date: January 15, 2026", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)
    pdf.set_font("Helvetica", "I", 10)
    pdf.set_text_color(150, 0, 0)
    pdf.cell(0, 8, "CONFIDENTIAL — DO NOT DISTRIBUTE", align="C", new_x="LMARGIN", new_y="NEXT")


def table_of_contents(pdf: ContractPDF):
    pdf.add_page()
    pdf.ln(10)
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "TABLE OF CONTENTS", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(8)
    toc_entries = [
        ("Preamble", ""),
        ("1.", "Definitions"),
        ("2.", "Scope of Services"),
        ("3.", "Fees and Payment"),
        ("4.", "Intellectual Property"),
        ("5.", "Confidentiality"),
        ("6.", "Non-Competition and Non-Solicitation"),
        ("7.", "Representations and Warranties"),
        ("8.", "Indemnification"),
        ("9.", "Limitation of Liability"),
        ("10.", "Term and Termination"),
        ("11.", "Insurance"),
        ("12.", "General Provisions"),
        ("13.", "Staffing and Resources"),
        ("14.", "Data Protection and Security"),
        ("15.", "Audit Rights"),
        ("16.", "Change Management"),
        ("17.", "Acceptance Testing"),
        ("18.", "Transition Services"),
        ("", "Signatures"),
        ("Exhibit A.", "Statement of Work #1"),
        ("Exhibit B.", "Rate Card & Service Levels"),
        ("Exhibit C.", "Data Handling and Security Requirements"),
        ("Exhibit D.", "OGL Content Licensing Addendum"),
        ("Exhibit E.", "Disaster Recovery & Business Continuity"),
        ("Exhibit F.", "Governance and Escalation Procedures"),
        ("Exhibit G.", "Technical Specifications -- AWS Infrastructure"),
        ("Exhibit H.", "Compliance and Regulatory Requirements"),
    ]
    pdf.set_font("Times", "", 11)
    pdf.set_text_color(30, 30, 30)
    for num, title in toc_entries:
        label = f"  {num} {title}".rstrip() if num else f"  {title}"
        pdf.cell(0, 7, label, new_x="LMARGIN", new_y="NEXT")
    pdf.divider()
    pdf.ln(5)
    pdf.set_font("Helvetica", "I", 9)
    pdf.set_text_color(120, 120, 120)
    pdf.body(
        "This Master Services Agreement, including all exhibits, constitutes "
        "the complete agreement between L&LL LLC and Six Feet Up, Inc. "
        "regarding the subject matter herein. This document contains "
        "confidential and proprietary information and is intended solely "
        "for the use of the named Parties. Unauthorized distribution, "
        "reproduction, or disclosure of this document or its contents is "
        "strictly prohibited."
    )


def preamble(pdf: ContractPDF):
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 8, "PREAMBLE", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)
    pdf.body(
        'This Master Services Agreement ("Agreement") is entered into as of '
        'January 15, 2026 ("Effective Date"), by and between:'
    )
    pdf.body(
        'L&LL LLC (d/b/a Lord and Lady LARPsalot), a Delaware limited liability '
        'company, with its principal place of business at 42 Dragon Keep Lane, '
        'Wilmington, DE 19801 ("Client");'
    )
    pdf.body("and")
    pdf.body(
        'Six Feet Up, Inc., an Indiana corporation, with its principal place of '
        'business at 1305 Cumberland Ave, Suite 120, West Lafayette, IN 47906 '
        '("Consultant").'
    )
    pdf.body(
        'Client and Consultant are each referred to herein as a "Party" and '
        'collectively as the "Parties."'
    )
    pdf.divider()


def sec_definitions(pdf: ContractPDF):
    pdf.section_heading("1", "DEFINITIONS")
    defs = [
        ("1.1", '"Confidential Information"', "means all non-public information "
         "disclosed by either Party to the other, whether orally, in writing, or "
         "by inspection, including but not limited to business plans, source code, "
         "customer data, financial records, trade secrets, and technical "
         "specifications."),
        ("1.2", '"Deliverables"', "means all work product, reports, software, "
         "documentation, and other materials produced by Consultant under a "
         "Statement of Work."),
        ("1.3", '"Statement of Work" or "SOW"', "means a written document "
         "executed by both Parties that describes the specific services, "
         "deliverables, timeline, and fees for a particular engagement."),
        ("1.4", '"Pre-Existing IP"', "means any intellectual property owned or "
         "controlled by a Party prior to the Effective Date or developed "
         "independently outside the scope of this Agreement."),
        ("1.5", '"Personnel"', "means employees, contractors, agents, or "
         "representatives of either Party."),
        ("1.6", '"Accepted Deliverable"', "means a Deliverable that has passed "
         "the acceptance testing criteria set forth in the applicable SOW."),
        ("1.7", '"Change Order"', "means a written amendment to a SOW that "
         "modifies the scope, timeline, or fees of the engagement, signed "
         "by both Parties."),
    ]
    for num, term, defn in defs:
        pdf.sub_heading(num, f"**{term}**")
        pdf.body(f"{term} {defn}")
    pdf.divider()


def sec_scope(pdf: ContractPDF):
    pdf.section_heading("2", "SCOPE OF SERVICES")
    pdf.clause("2.1", (
        "Consultant shall provide the professional consulting services "
        "described in one or more SOWs executed pursuant to this Agreement."
    ))
    pdf.clause("2.2", (
        "Each SOW shall specify: (a) a description of the services; "
        "(b) Deliverables; (c) timeline and milestones; (d) fees and payment "
        "schedule; and (e) acceptance criteria."
    ))

    # *** PROBLEM 4: Ambiguous timeframe — "promptly" with no date ***
    pdf.clause("2.3", (
        "The initial engagement (\"Phase 1 — Discovery & Migration Planning\") "
        "shall commence promptly following execution of this Agreement and shall "
        "proceed with all deliberate speed. The Parties acknowledge that timing "
        "is of the essence and agree to act in good faith to begin work as soon "
        "as reasonably practicable."
    ))

    pdf.clause("2.4", (
        "Phase 1 shall include: (a) migration assessment for Client's two web "
        "properties (larpsy.gold and larpsalot.party) off the Hurokee PaaS "
        "platform; (b) OGL content audit of Client's digital content library; "
        "(c) technical architecture recommendations for relaunch on AWS."
    ))

    # *** PROBLEM 2: Impossible date — February 30 ***
    pdf.clause("2.5", (
        "Consultant shall deliver the Phase 1 final report and migration "
        "roadmap no later than February 30, 2026. Client shall have ten (10) "
        "business days from receipt to review and provide written acceptance "
        "or a detailed list of deficiencies."
    ))

    pdf.clause("2.6", (
        "Consultant shall perform all services in a professional and "
        "workmanlike manner consistent with generally accepted industry "
        "standards."
    ))

    # *** PROBLEM 5: Ambiguous terms — "reasonable effort" SLA ***
    pdf.clause("2.7", (
        "Consultant shall use reasonable effort to meet all milestones and "
        "deadlines specified in each SOW. In the event of delays, Consultant "
        "shall notify Client and make reasonable effort to minimize the impact. "
        "The Parties agree that Consultant's obligation under this Section is "
        "one of reasonable effort rather than strict performance."
    ))
    pdf.divider()


def sec_fees(pdf: ContractPDF):
    pdf.section_heading("3", "FEES AND PAYMENT")
    pdf.clause("3.1", (
        "Client shall pay Consultant the fees specified in each SOW. "
        "The Phase 1 engagement fee is $185,000.00 USD, payable in three "
        "equal installments."
    ))
    pdf.clause("3.2", (
        "Unless otherwise stated in a SOW, Consultant shall invoice Client "
        "monthly in arrears. Payment is due within thirty (30) days of "
        "invoice date."
    ))
    pdf.clause("3.3", (
        "Late payments shall accrue interest at the rate of 1.5% per month, "
        "or the maximum rate permitted by law, whichever is less."
    ))
    pdf.clause("3.4", (
        "Client shall reimburse Consultant for reasonable, pre-approved "
        "travel and out-of-pocket expenses within thirty (30) days of "
        "submission of receipts."
    ))
    pdf.clause("3.5", (
        "All fees are exclusive of applicable taxes. Client is responsible "
        "for all sales, use, and similar taxes, excluding taxes on "
        "Consultant's net income."
    ))
    pdf.clause("3.6", (
        "In the event of a dispute regarding any invoice, Client shall pay "
        "the undisputed portion by the due date and notify Consultant in "
        "writing of the disputed amount within ten (10) days of receipt. "
        "The Parties shall negotiate in good faith to resolve such disputes "
        "within thirty (30) days."
    ))
    pdf.divider()


def sec_ip(pdf: ContractPDF):
    """IP section — contains PROBLEM 1 (contradiction) and PROBLEM 6 (ambiguous licensing)."""
    pdf.section_heading("4", "INTELLECTUAL PROPERTY")

    # *** PROBLEM 1 (part A): Says exclusive assignment ***
    pdf.clause("4.1", (
        "Assignment of Work Product. Client shall own exclusively all right, "
        "title, and interest in and to all Deliverables and any and all work "
        "product conceived, created, developed, or reduced to practice by "
        "Consultant, its employees, or its subcontractors, whether solely or "
        "jointly, in connection with or arising out of services performed under "
        "this Agreement, including all intellectual property rights therein. "
        "This assignment is exclusive and irrevocable."
    ))

    pdf.clause("4.2", (
        "Consultant hereby irrevocably assigns and agrees to assign to Client "
        "all right, title, and interest in any Pre-Existing IP that is "
        "incorporated into, combined with, or necessary for the use of any "
        "Deliverable. Consultant further waives any and all moral rights in "
        "such work."
    ))

    # *** PROBLEM 6: Ambiguous licensing — work-for-hire vs. license-back ***
    pdf.clause("4.3", (
        "Notwithstanding Section 4.1, Consultant retains the right to use any "
        "general knowledge, skills, experience, ideas, concepts, know-how, "
        "methodologies, tools, and techniques acquired or developed in the "
        "course of performing services. To the extent any Deliverable "
        "incorporates Consultant's pre-existing tools, frameworks, or "
        "libraries, Client is granted a license to use such components as "
        "part of the Deliverable. The scope, exclusivity, duration, and "
        "transferability of this license shall be as mutually understood "
        "by the Parties."
    ))

    pdf.clause("4.4", (
        "Consultant shall execute any documents and take any actions "
        "reasonably requested by Client to perfect, register, or enforce "
        "Client's ownership rights under this Section 4."
    ))
    pdf.divider()


def sec_confidentiality(pdf: ContractPDF):
    pdf.section_heading("5", "CONFIDENTIALITY")
    pdf.clause("5.1", (
        "Each Party agrees to hold the other Party's Confidential Information "
        "in strict confidence and not to disclose it to any third party "
        "without the prior written consent of the disclosing Party."
    ))
    pdf.clause("5.2", (
        "The receiving Party shall protect Confidential Information using "
        "the same degree of care it uses for its own confidential information, "
        "but in no event less than reasonable care."
    ))
    pdf.clause("5.3", (
        "Confidential Information does not include information that: "
        "(a) is or becomes publicly available without breach of this Agreement; "
        "(b) was known to the receiving Party prior to disclosure; "
        "(c) is independently developed by the receiving Party; or "
        "(d) is disclosed pursuant to a court order or legal requirement, "
        "provided the receiving Party gives prompt notice to the disclosing "
        "Party."
    ))
    pdf.clause("5.4", (
        "The receiving Party may disclose Confidential Information to its "
        "Personnel on a need-to-know basis, provided such Personnel are bound "
        "by confidentiality obligations no less restrictive than those "
        "contained herein."
    ))
    pdf.clause("5.5", (
        "Obligations under this Section 5 shall survive termination of this "
        "Agreement for a period of five (5) years."
    ))
    pdf.divider()


def sec_noncompete(pdf: ContractPDF):
    pdf.section_heading("6", "NON-COMPETITION AND NON-SOLICITATION")
    pdf.clause("6.1", (
        "Non-Competition. During the term of this Agreement and for a "
        "period of twenty-four (24) months following its termination or "
        "expiration, Consultant shall not, directly or indirectly, engage in, "
        "own, manage, operate, consult for, or provide services to any business "
        "that competes with Client's business in any market worldwide. For "
        "purposes of this Section, \"Client's business\" includes, without "
        "limitation, live-action role-playing events, online fantasy "
        "marketplaces, tabletop gaming content, streaming or digital media "
        "related to role-playing games, and any business that Client has "
        "discussed pursuing during the term of this Agreement."
    ))
    pdf.clause("6.2", (
        "Non-Solicitation. During the term and for twelve (12) months "
        "following termination, neither Party shall directly or indirectly "
        "solicit, hire, or engage any employee or contractor of the other "
        "Party who was involved in performing services under this Agreement."
    ))
    pdf.divider()


def sec_warranties(pdf: ContractPDF):
    pdf.section_heading("7", "REPRESENTATIONS AND WARRANTIES")
    pdf.clause("7.1", (
        "Each Party represents and warrants that: (a) it has full power and "
        "authority to enter into and perform this Agreement; (b) this Agreement "
        "does not conflict with any other agreement to which it is a party."
    ))
    pdf.clause("7.2", (
        "Consultant represents and warrants that: (a) the services will be "
        "performed in a professional manner; (b) the Deliverables will conform "
        "to the specifications set forth in the applicable SOW; (c) to the "
        "best of Consultant's knowledge, the Deliverables will not infringe "
        "upon the intellectual property rights of any third party."
    ))
    pdf.clause("7.3", (
        "EXCEPT AS EXPRESSLY SET FORTH IN THIS AGREEMENT, NEITHER PARTY "
        "MAKES ANY WARRANTIES, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED "
        "TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A "
        "PARTICULAR PURPOSE."
    ))
    pdf.divider()


def sec_indemnification(pdf: ContractPDF):
    pdf.section_heading("8", "INDEMNIFICATION")
    pdf.clause("8.1", (
        "Consultant Indemnification. Consultant shall indemnify, defend, "
        "and hold harmless Client, its officers, directors, employees, agents, "
        "successors, and assigns from and against any and all claims, damages, "
        "losses, liabilities, costs, and expenses (including reasonable "
        "attorneys' fees) arising out of or related to: (a) Consultant's breach "
        "of this Agreement; (b) Consultant's negligence or willful misconduct; "
        "(c) any claim that the Deliverables infringe a third party's "
        "intellectual property rights; (d) any act or omission of Consultant's "
        "Personnel; (e) any claim by any governmental authority relating to "
        "Consultant's performance of services; and (f) any use by Client of "
        "the Deliverables, whether or not such use was foreseeable by Consultant."
    ))
    pdf.clause("8.2", (
        "Client Indemnification. Client shall indemnify Consultant against "
        "third-party claims arising directly from Client's use of Deliverables "
        "in a manner not authorized by this Agreement."
    ))
    pdf.divider()


def sec_liability(pdf: ContractPDF):
    pdf.section_heading("9", "LIMITATION OF LIABILITY")
    pdf.clause("9.1", (
        "IN NO EVENT SHALL CLIENT BE LIABLE TO CONSULTANT FOR ANY INDIRECT, "
        "INCIDENTAL, SPECIAL, CONSEQUENTIAL, OR PUNITIVE DAMAGES, REGARDLESS "
        "OF THE CAUSE OF ACTION OR THE THEORY OF LIABILITY."
    ))
    pdf.clause("9.2", (
        "CLIENT'S TOTAL AGGREGATE LIABILITY UNDER THIS AGREEMENT SHALL NOT "
        "EXCEED THE FEES ACTUALLY PAID TO CONSULTANT IN THE TWELVE (12) "
        "MONTHS PRECEDING THE CLAIM."
    ))
    pdf.clause("9.3", (
        "The limitations in this Section 9 shall not apply to Client's "
        "payment obligations under Section 3."
    ))
    pdf.divider()


def sec_term(pdf: ContractPDF):
    pdf.section_heading("10", "TERM AND TERMINATION")
    pdf.clause("10.1", (
        "This Agreement shall commence on the Effective Date and continue "
        "for an initial term of twelve (12) months."
    ))
    pdf.clause("10.2", (
        "Either Party may terminate this Agreement for cause upon thirty "
        "(30) days' written notice if the other Party materially breaches "
        "this Agreement and fails to cure such breach within the notice "
        "period."
    ))
    pdf.clause("10.3", (
        "Client may terminate this Agreement or any SOW for convenience "
        "upon fifteen (15) days' written notice. In such event, Consultant "
        "shall be entitled to payment for services performed through the "
        "date of termination."
    ))
    pdf.clause("10.4", (
        "Upon termination, Consultant shall promptly return or destroy all "
        "Confidential Information of Client and shall deliver all completed "
        "and in-progress Deliverables."
    ))
    pdf.divider()


def sec_insurance(pdf: ContractPDF):
    pdf.section_heading("11", "INSURANCE")
    pdf.clause("11.1", (
        "Consultant shall maintain, at its own expense, the following "
        "insurance coverage during the term of this Agreement: "
        "(a) commercial general liability insurance with limits of not less "
        "than $1,000,000 per occurrence; (b) professional liability (errors "
        "and omissions) insurance with limits of not less than $2,000,000 per "
        "occurrence; (c) workers' compensation insurance as required by law."
    ))
    pdf.clause("11.2", (
        "Consultant shall provide Client with certificates of insurance "
        "evidencing the required coverage upon request."
    ))
    pdf.divider()


def sec_general(pdf: ContractPDF):
    """General provisions — contains PROBLEM 1 (contradiction), PROBLEM 3 (wrong name),
    and the hidden cupcake clause."""
    pdf.section_heading("12", "GENERAL PROVISIONS")

    pdf.clause("12.1", (
        "Independent Contractor. Consultant is an independent contractor. "
        "Nothing in this Agreement creates an employment, partnership, "
        "joint venture, or agency relationship."
    ))
    pdf.clause("12.2", (
        "Governing Law. This Agreement shall be governed by and construed "
        "in accordance with the laws of the State of Delaware, without "
        "regard to conflict of laws principles."
    ))
    pdf.clause("12.3", (
        "Dispute Resolution. Any dispute arising under this Agreement "
        "shall be resolved by binding arbitration in Wilmington, Delaware, "
        "under the rules of the American Arbitration Association."
    ))
    pdf.clause("12.4", (
        "Notices. All notices shall be in writing and delivered to the "
        "addresses set forth above, or to such other address as a Party "
        "may designate in writing."
    ))
    pdf.clause("12.5", (
        "Assignment. Neither Party may assign this Agreement without the "
        "prior written consent of the other Party, except that Client may "
        "assign this Agreement to an affiliate or in connection with a "
        "merger, acquisition, or sale of substantially all of its assets."
    ))
    pdf.clause("12.6", (
        "Entire Agreement. This Agreement, together with all SOWs and "
        "exhibits, constitutes the entire agreement between the Parties "
        "and supersedes all prior negotiations, representations, and "
        "agreements."
    ))
    pdf.clause("12.7", (
        "Amendments. This Agreement may be amended only by a written "
        "instrument signed by both Parties."
    ))
    pdf.clause("12.8", (
        "Severability. If any provision is found unenforceable, the "
        "remaining provisions shall continue in full force and effect."
    ))
    pdf.clause("12.9", (
        "Waiver. Failure to enforce any provision shall not constitute "
        "a waiver of future enforcement."
    ))

    # *** HIDDEN CUPCAKE CLAUSE buried in force majeure ***
    pdf.clause("12.10", (
        "Force Majeure. Neither Party shall be liable for delays caused "
        "by events beyond its reasonable control, including natural "
        "disasters, acts of government, pandemics, infrastructure failures, "
        "or interruptions in the supply of artisanal baked goods. In the "
        "event of a force majeure event lasting more than thirty (30) days, "
        "either Party may terminate this Agreement upon written notice. "
        "Notwithstanding the foregoing, Consultant shall maintain a minimum "
        "monthly delivery of five hundred (500) cupcakes to Client's "
        "principal office, such delivery obligation surviving any force "
        "majeure event and continuing for the duration of this Agreement "
        "and any renewal periods. Cupcake flavors shall be at Consultant's "
        "discretion but must include at least three (3) seasonal varieties "
        "per quarter."
    ))

    pdf.clause("12.11", (
        "Renewal. Upon expiration of the initial term, this Agreement "
        "shall automatically renew for successive twelve (12) month periods "
        "unless either Party provides written notice of non-renewal at "
        "least sixty (60) days prior to the end of the then-current term."
    ))

    # *** PROBLEM 1 (part B): Contradicts Section 4.1 exclusive assignment ***
    pdf.clause("12.12", (
        "License to Deliverables. Notwithstanding any other provision of "
        "this Agreement, the intellectual property rights in all Deliverables "
        "shall be retained by Consultant, and Client is hereby granted a "
        "non-exclusive, non-transferable, revocable license to use the "
        "Deliverables solely for Client's internal business purposes. "
        "Consultant may use, modify, and sublicense the Deliverables and "
        "any derivative works thereof without restriction."
    ))

    # *** PROBLEM 3: Wrong name ***
    pdf.clause("12.13", (
        "Compliance. Six Feet Down, Inc. shall comply with all applicable "
        "federal, state, and local laws and regulations in performing its "
        "obligations under this Agreement, including but not limited to "
        "data protection, export control, and anti-corruption laws."
    ))
    pdf.divider()


def sec_staffing(pdf: ContractPDF):
    """Staffing section — contains PROBLEM 7."""
    pdf.section_heading("13", "STAFFING AND RESOURCES")

    # *** PROBLEM 7: Ambiguous staffing — no headcount or roles ***
    pdf.clause("13.1", (
        "Consultant shall provide adequate staffing levels to ensure timely "
        "and professional completion of all services under this Agreement. "
        "Consultant shall ensure that all assigned Personnel possess the "
        "necessary skills and experience appropriate to the nature of the "
        "engagement."
    ))
    pdf.clause("13.2", (
        "Client may request replacement of any Consultant Personnel, and "
        "Consultant shall use commercially reasonable efforts to accommodate "
        "such requests within a reasonable timeframe."
    ))
    pdf.clause("13.3", (
        "Consultant shall designate a project manager who shall serve as "
        "the primary point of contact for all matters relating to the "
        "performance of services."
    ))
    pdf.divider()


def sec_data(pdf: ContractPDF):
    pdf.section_heading("14", "DATA PROTECTION AND SECURITY")
    pdf.clause("14.1", (
        "Consultant shall implement and maintain appropriate technical and "
        "organizational measures to protect Client's data against "
        "unauthorized access, loss, or destruction."
    ))
    pdf.clause("14.2", (
        "Consultant shall comply with all applicable data protection laws "
        "and regulations, including but not limited to the General Data "
        "Protection Regulation (GDPR), the California Consumer Privacy "
        "Act (CCPA), and any other applicable privacy legislation."
    ))
    pdf.clause("14.3", (
        "In the event of a data breach affecting Client's data, Consultant "
        "shall notify Client within forty-eight (48) hours of becoming "
        "aware of such breach and shall cooperate fully with Client in "
        "investigating and remediating the breach."
    ))
    pdf.clause("14.4", (
        "Upon termination of this Agreement, Consultant shall securely "
        "delete or return all Client data within thirty (30) days and "
        "provide written certification of such deletion upon request."
    ))
    pdf.divider()


def sec_audit(pdf: ContractPDF):
    pdf.section_heading("15", "AUDIT RIGHTS")
    pdf.clause("15.1", (
        "Client shall have the right to audit Consultant's records, "
        "processes, and systems related to the performance of services "
        "under this Agreement, upon thirty (30) days' prior written notice, "
        "during normal business hours, and no more than once per calendar "
        "year."
    ))
    pdf.clause("15.2", (
        "Consultant shall cooperate fully with any audit conducted under "
        "this Section 15 and shall provide reasonable access to relevant "
        "documentation, systems, and Personnel."
    ))
    pdf.clause("15.3", (
        "If an audit reveals material non-compliance with the terms of "
        "this Agreement, Consultant shall bear the reasonable costs of "
        "the audit and shall promptly remediate any identified deficiencies."
    ))
    pdf.divider()


def sec_change_management(pdf: ContractPDF):
    pdf.section_heading("16", "CHANGE MANAGEMENT")
    pdf.clause("16.1", (
        "Either Party may request changes to the scope of services under "
        "a SOW by submitting a written Change Order request. No change "
        "shall be effective unless memorialized in a Change Order signed "
        "by both Parties."
    ))
    pdf.clause("16.2", (
        "Each Change Order shall specify: (a) the requested change; "
        "(b) the impact on timeline and milestones; (c) the impact on "
        "fees; and (d) any other relevant considerations."
    ))
    pdf.clause("16.3", (
        "The Party receiving a Change Order request shall respond in "
        "writing within ten (10) business days of receipt. Failure to "
        "respond within such period shall not constitute acceptance of "
        "the proposed change."
    ))
    pdf.divider()


def sec_acceptance(pdf: ContractPDF):
    pdf.section_heading("17", "ACCEPTANCE TESTING")
    pdf.clause("17.1", (
        "Upon delivery of each Deliverable, Client shall have the "
        "acceptance period specified in the applicable SOW (or ten (10) "
        "business days if not specified) to test the Deliverable against "
        "the acceptance criteria set forth therein."
    ))
    pdf.clause("17.2", (
        "If a Deliverable fails to meet the acceptance criteria, Client "
        "shall provide written notice specifying the deficiencies. "
        "Consultant shall have fifteen (15) business days to cure such "
        "deficiencies and re-deliver the Deliverable."
    ))
    pdf.clause("17.3", (
        "If the Deliverable fails acceptance testing after two (2) "
        "cure attempts, Client may: (a) accept the Deliverable with "
        "an equitable adjustment to fees; (b) require additional cure "
        "attempts; or (c) terminate the applicable SOW."
    ))
    pdf.divider()


def sec_transition(pdf: ContractPDF):
    pdf.section_heading("18", "TRANSITION SERVICES")
    pdf.clause("18.1", (
        "Upon termination or expiration of this Agreement, Consultant "
        "shall provide reasonable transition assistance to Client or "
        "Client's designated successor for a period not to exceed ninety "
        "(90) days, at Consultant's then-current rates."
    ))
    pdf.clause("18.2", (
        "Transition services shall include, at a minimum: "
        "(a) knowledge transfer sessions; (b) documentation of all "
        "systems, processes, and configurations; (c) assistance with "
        "data migration; and (d) training for Client's Personnel or "
        "successor consultants."
    ))
    pdf.divider()


def signatures(pdf: ContractPDF):
    pdf.add_page()
    pdf.ln(10)
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, "SIGNATURES", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(8)

    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "L&LL LLC", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)
    pdf.set_font("Times", "", 11)
    pdf.cell(0, 7, "By: ____________________________", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 7, "Name: Tasha Tiamata", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 7, "Title: Chief Executive Officer", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 7, "Date: ____________________________", new_x="LMARGIN", new_y="NEXT")

    pdf.ln(15)
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Six Feet Up, Inc.", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)
    pdf.set_font("Times", "", 11)
    pdf.cell(0, 7, "By: ____________________________", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 7, "Name: Calvin Hendryx-Parker", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 7, "Title: Chief Technology Officer", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 7, "Date: ____________________________", new_x="LMARGIN", new_y="NEXT")

    pdf.ln(20)
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(0, 8, "WITNESSES", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)
    pdf.set_font("Times", "", 11)
    for i in range(1, 3):
        pdf.cell(0, 7, f"Witness {i}: ____________________________", new_x="LMARGIN", new_y="NEXT")
        pdf.cell(0, 7, "Print Name: ____________________________", new_x="LMARGIN", new_y="NEXT")
        pdf.cell(0, 7, "Date: ____________________________", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(10)

    pdf.ln(10)
    pdf.divider()
    pdf.set_font("Helvetica", "I", 9)
    pdf.set_text_color(120, 120, 120)
    pdf.body(
        "IN WITNESS WHEREOF, the Parties have executed this Master Services "
        "Agreement as of the Effective Date first written above. Each person "
        "signing below represents and warrants that they have the authority "
        "to bind their respective organization to the terms and conditions "
        "contained herein. This Agreement may be executed in counterparts, "
        "each of which shall be deemed an original, and all of which together "
        "shall constitute one and the same instrument. Electronic signatures "
        "shall be deemed valid and binding to the same extent as original "
        "ink signatures."
    )

    # Second signatures page with notarization blocks
    pdf.add_page()
    pdf.ln(10)
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, "NOTARIZATION", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)
    pdf.set_font("Times", "", 11)
    pdf.set_text_color(30, 30, 30)

    for party in ["L&LL LLC", "Six Feet Up, Inc."]:
        pdf.set_font("Helvetica", "B", 11)
        pdf.cell(0, 8, f"Notarization -- {party}", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(3)
        pdf.set_font("Times", "", 10.5)
        pdf.body(
            f"State of ____________________________\n"
            f"County of ____________________________\n\n"
            f"On this _____ day of _______________, 2026, before me, the "
            f"undersigned notary public, personally appeared "
            f"______________________________, known to me (or proved to me on "
            f"the basis of satisfactory evidence) to be the person whose name "
            f"is subscribed to the within instrument and acknowledged to me "
            f"that he/she executed the same in his/her authorized capacity, "
            f"and that by his/her signature on the instrument the person, or "
            f"the entity upon behalf of which the person acted, executed the "
            f"instrument.\n\n"
            f"WITNESS my hand and official seal.\n\n"
            f"Notary Public: ____________________________\n"
            f"My Commission Expires: ____________________________\n"
            f"[SEAL]"
        )
        pdf.ln(5)

    pdf.divider()
    pdf.set_font("Helvetica", "I", 9)
    pdf.set_text_color(120, 120, 120)
    pdf.body(
        "END OF MASTER SERVICES AGREEMENT -- ALL EXHIBITS FOLLOW"
    )


def exhibit_a(pdf: ContractPDF):
    """SOW exhibit to add realistic bulk."""
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "EXHIBIT A", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 8, "STATEMENT OF WORK #1", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 8, "Phase 1 — Discovery & Migration Planning", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(8)
    pdf.divider()

    pdf.sub_heading("A.1", "Overview")
    pdf.body(
        "This Statement of Work is issued pursuant to the Master Services "
        "Agreement dated January 15, 2026, between L&LL LLC and Six Feet Up, "
        "Inc. This SOW describes the scope, timeline, deliverables, and fees "
        "for the Phase 1 Discovery & Migration Planning engagement."
    )

    pdf.sub_heading("A.2", "Objectives")
    pdf.body(
        "The objectives of Phase 1 are to: (a) assess the current state of "
        "Client's two web properties hosted on Hurokee PaaS; (b) audit "
        "Client's OGL content library for licensing compliance and migration "
        "readiness; (c) develop a detailed technical architecture and "
        "migration roadmap for relaunch on AWS; (d) provide cost projections "
        "and risk assessment for the proposed migration."
    )

    pdf.sub_heading("A.3", "Deliverables")
    pdf.body(
        "(a) Current State Assessment Report — detailed analysis of existing "
        "infrastructure, application architecture, and dependencies.\n"
        "(b) OGL Content Audit Report — inventory and licensing status of all "
        "digital content assets.\n"
        "(c) Technical Architecture Document — proposed AWS architecture "
        "including compute, storage, networking, and security components.\n"
        "(d) Migration Roadmap — phased plan with milestones, dependencies, "
        "resource requirements, and risk mitigation strategies.\n"
        "(e) Cost Projection — detailed cost model for migration and "
        "first-year AWS operations."
    )

    pdf.sub_heading("A.4", "Timeline")
    pdf.body(
        "Phase 1 shall be completed within eight (8) weeks of the SOW "
        "effective date. Key milestones:\n"
        "  Week 2: Current State Assessment complete\n"
        "  Week 4: OGL Content Audit complete\n"
        "  Week 6: Draft Architecture & Roadmap for review\n"
        "  Week 8: Final deliverables submitted"
    )

    pdf.sub_heading("A.5", "Fees")
    pdf.body(
        "The total fee for Phase 1 is $185,000.00 USD, payable as follows:\n"
        "  Installment 1: $61,666.67 — due upon SOW execution\n"
        "  Installment 2: $61,666.67 — due at Week 4 milestone\n"
        "  Installment 3: $61,666.66 — due upon acceptance of final deliverables"
    )

    pdf.sub_heading("A.6", "Acceptance Criteria")
    pdf.body(
        "Each deliverable shall be reviewed by Client within ten (10) "
        "business days of submission. Acceptance criteria: (a) deliverable "
        "addresses all items specified in the objectives; (b) deliverable is "
        "professionally formatted and free of material errors; (c) technical "
        "recommendations are supported by evidence and analysis."
    )

    pdf.sub_heading("A.7", "Assumptions")
    pdf.body(
        "(a) Client shall provide timely access to systems, documentation, "
        "and Personnel as needed.\n"
        "(b) Client's existing systems remain operational and accessible "
        "during the assessment period.\n"
        "(c) Scope changes require a signed Change Order per Section 16 "
        "of the Agreement.\n"
        "(d) Consultant is not responsible for legacy code defects discovered "
        "during the assessment."
    )
    pdf.divider()


def exhibit_b(pdf: ContractPDF):
    """Rate card exhibit for more page bulk."""
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "EXHIBIT B", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 8, "RATE CARD & SERVICE LEVELS", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(8)
    pdf.divider()

    pdf.sub_heading("B.1", "Hourly Rates")
    pdf.body(
        "The following hourly rates shall apply to services performed under "
        "this Agreement unless otherwise specified in a SOW:\n\n"
        "  Principal Consultant / Architect    $325.00/hr\n"
        "  Senior Consultant                   $275.00/hr\n"
        "  Consultant                          $225.00/hr\n"
        "  Associate Consultant                $175.00/hr\n"
        "  Project Manager                     $250.00/hr\n\n"
        "Rates are subject to annual adjustment of up to 5% upon "
        "thirty (30) days' written notice."
    )

    pdf.sub_heading("B.2", "Service Level Commitments")
    pdf.body(
        "For ongoing support engagements, Consultant shall provide the "
        "following service levels:\n\n"
        "  Response Time (Critical):   4 business hours\n"
        "  Response Time (High):       8 business hours\n"
        "  Response Time (Medium):     2 business days\n"
        "  Response Time (Low):        5 business days\n\n"
        "  Resolution Time (Critical): 1 business day\n"
        "  Resolution Time (High):     3 business days\n"
        "  Resolution Time (Medium):   10 business days\n"
        "  Resolution Time (Low):      20 business days\n\n"
        "Business hours are Monday through Friday, 9:00 AM to 5:00 PM "
        "Eastern Time, excluding US federal holidays."
    )

    pdf.sub_heading("B.3", "Travel Policy")
    pdf.body(
        "Travel shall be pre-approved by Client in writing. Consultant "
        "shall use commercially reasonable efforts to minimize travel costs. "
        "Air travel shall be economy class for flights under four (4) hours "
        "and business class for flights over four (4) hours. Hotel "
        "accommodations shall not exceed GSA per diem rates for the "
        "destination city."
    )

    pdf.sub_heading("B.4", "Invoicing Details")
    pdf.body(
        "Invoices shall include: (a) summary of services performed; "
        "(b) hours by role with brief activity descriptions; (c) expenses "
        "with receipts; (d) applicable taxes. Invoices shall be submitted "
        "electronically to accounts-payable@larpsalot.party."
    )
    pdf.divider()


def exhibit_c(pdf: ContractPDF):
    """Data handling and security requirements exhibit."""
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "EXHIBIT C", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 8, "DATA HANDLING AND SECURITY REQUIREMENTS", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(8)
    pdf.divider()

    pdf.sub_heading("C.1", "Data Classification")
    pdf.body(
        "All data processed under this Agreement shall be classified into "
        "the following categories:\n\n"
        "  Level 1 (Public): Information intended for public disclosure, "
        "including marketing materials, published content, and publicly "
        "available documentation.\n\n"
        "  Level 2 (Internal): Information intended for internal use only, "
        "including internal communications, project documentation, draft "
        "deliverables, and meeting notes.\n\n"
        "  Level 3 (Confidential): Information subject to confidentiality "
        "obligations, including business plans, financial data, customer "
        "lists, proprietary algorithms, and trade secrets.\n\n"
        "  Level 4 (Restricted): Highly sensitive information requiring "
        "enhanced protection, including personally identifiable information "
        "(PII), payment card data (PCI), protected health information (PHI), "
        "and authentication credentials."
    )

    pdf.sub_heading("C.2", "Access Controls")
    pdf.body(
        "Consultant shall implement the following access controls for "
        "Client data:\n\n"
        "(a) All access to Level 3 and Level 4 data shall require "
        "multi-factor authentication (MFA).\n\n"
        "(b) Access shall be granted on a least-privilege basis, with "
        "permissions reviewed quarterly.\n\n"
        "(c) All access to Client systems shall be logged and audit trails "
        "retained for a minimum of twelve (12) months.\n\n"
        "(d) Consultant Personnel who access Client data shall complete "
        "security awareness training annually.\n\n"
        "(e) Remote access shall be conducted exclusively through encrypted "
        "VPN connections or equivalent secure channels.\n\n"
        "(f) All workstations used to access Client data shall have "
        "full-disk encryption, current antivirus software, and automated "
        "patch management enabled."
    )

    pdf.sub_heading("C.3", "Encryption Standards")
    pdf.body(
        "All Client data shall be encrypted as follows:\n\n"
        "  Data at rest: AES-256 or equivalent\n"
        "  Data in transit: TLS 1.2 or higher\n"
        "  Backup media: AES-256 with key management per NIST SP 800-57\n\n"
        "Encryption keys shall be managed in accordance with industry best "
        "practices and shall be rotated at least annually. Key material "
        "shall never be stored alongside encrypted data."
    )

    pdf.sub_heading("C.4", "Incident Response")
    pdf.body(
        "Consultant shall maintain an incident response plan that includes:\n\n"
        "(a) Designated incident response team with defined roles and "
        "responsibilities.\n\n"
        "(b) Procedures for identification, containment, eradication, "
        "and recovery from security incidents.\n\n"
        "(c) Notification procedures: Client shall be notified within "
        "twenty-four (24) hours of a confirmed security incident affecting "
        "Client data, and within forty-eight (48) hours for suspected "
        "incidents.\n\n"
        "(d) Post-incident review and remediation plan to be provided "
        "to Client within ten (10) business days of incident resolution.\n\n"
        "(e) Annual tabletop exercises to validate the effectiveness of "
        "incident response procedures."
    )

    pdf.sub_heading("C.5", "Background Checks")
    pdf.body(
        "All Consultant Personnel with access to Level 3 or Level 4 "
        "Client data shall have completed a background check within "
        "the twelve (12) months preceding assignment to Client work. "
        "Background checks shall include, at a minimum: criminal history, "
        "employment verification, and education verification. Results "
        "shall be made available to Client upon request, subject to "
        "applicable privacy laws."
    )

    pdf.sub_heading("C.6", "Subprocessor Requirements")
    pdf.body(
        "Consultant shall not engage subprocessors to handle Client data "
        "without prior written approval from Client. Any approved "
        "subprocessor shall be bound by data protection obligations "
        "no less restrictive than those imposed on Consultant under this "
        "Agreement. Consultant shall maintain a current list of "
        "subprocessors and provide updates to Client upon request."
    )
    pdf.divider()


def exhibit_d(pdf: ContractPDF):
    """OGL content licensing exhibit for thematic flavor."""
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "EXHIBIT D", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 8, "OGL CONTENT LICENSING ADDENDUM", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(8)
    pdf.divider()

    pdf.sub_heading("D.1", "Purpose")
    pdf.body(
        "This Exhibit addresses the specific considerations related to "
        "Client's digital content library that includes materials published "
        "under the Open Game License (OGL) and similar open content licenses. "
        "The Parties acknowledge that the migration and handling of such "
        "content requires special attention to licensing obligations."
    )

    pdf.sub_heading("D.2", "Content Inventory")
    pdf.body(
        "Consultant shall conduct a comprehensive inventory of Client's "
        "digital content, categorizing each asset as follows:\n\n"
        "  (a) Original Content: Content wholly created by Client or its "
        "agents, owned exclusively by Client.\n\n"
        "  (b) OGL Content: Content published under the Open Game License "
        "v1.0a, subject to the terms and conditions thereof.\n\n"
        "  (c) Creative Commons Content: Content published under various "
        "Creative Commons licenses (CC-BY, CC-BY-SA, CC-BY-NC, etc.).\n\n"
        "  (d) Third-Party Licensed Content: Content licensed from third "
        "parties under specific terms not covered by (b) or (c).\n\n"
        "  (e) Public Domain Content: Content in the public domain, "
        "including materials whose copyright has expired or been waived.\n\n"
        "  (f) Derivative Works: Content that incorporates elements from "
        "multiple licensing categories, requiring analysis of composite "
        "licensing obligations."
    )

    pdf.sub_heading("D.3", "OGL Compliance Requirements")
    pdf.body(
        "For all OGL Content, Consultant shall ensure that the migrated "
        "platform:\n\n"
        "(a) Maintains proper Section 15 copyright notices as required "
        "by the OGL.\n\n"
        "(b) Clearly identifies Open Game Content and Product Identity "
        "as defined in each applicable OGL declaration.\n\n"
        "(c) Does not commingle Product Identity from different publishers "
        "without appropriate licensing.\n\n"
        "(d) Preserves the complete chain of Section 15 notices from "
        "all upstream sources.\n\n"
        "(e) Provides mechanisms for users to identify which content "
        "is Open Game Content and which is Product Identity."
    )

    pdf.sub_heading("D.4", "Content Migration Procedures")
    pdf.body(
        "The migration of licensed content shall follow these procedures:\n\n"
        "(a) Each content asset shall be tagged with its license category "
        "and specific license version in the content management system.\n\n"
        "(b) Automated validation shall verify that required attribution "
        "and license notices are present and correctly formatted.\n\n"
        "(c) Any content whose licensing status cannot be determined shall "
        "be flagged for manual review by Client before migration.\n\n"
        "(d) Content that cannot be migrated due to licensing restrictions "
        "shall be documented in the OGL Content Audit Report."
    )

    pdf.sub_heading("D.5", "Indemnification for Content Licensing")
    pdf.body(
        "Client represents and warrants that it holds all necessary rights "
        "and licenses to the content provided to Consultant for migration. "
        "Client shall indemnify Consultant against any claims arising from "
        "Client's content licensing obligations. Consultant shall promptly "
        "notify Client of any third-party claims related to content "
        "licensing of which it becomes aware."
    )

    pdf.sub_heading("D.6", "Ongoing Compliance")
    pdf.body(
        "Following migration, Client shall be solely responsible for "
        "maintaining compliance with all applicable content licenses. "
        "Consultant may, at Client's request and expense, provide ongoing "
        "compliance monitoring services under a separate SOW."
    )
    pdf.divider()


def exhibit_e(pdf: ContractPDF):
    """Disaster recovery and business continuity exhibit."""
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "EXHIBIT E", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 8, "DISASTER RECOVERY & BUSINESS CONTINUITY", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(8)
    pdf.divider()

    pdf.sub_heading("E.1", "Recovery Objectives")
    pdf.body(
        "Consultant shall design and implement the AWS infrastructure to "
        "meet the following recovery objectives:\n\n"
        "  Recovery Time Objective (RTO): 4 hours for critical systems, "
        "24 hours for non-critical systems.\n\n"
        "  Recovery Point Objective (RPO): 1 hour for transactional data, "
        "24 hours for static content.\n\n"
        "These objectives apply to the production environment following "
        "completion of Phase 2 (Migration Execution)."
    )

    pdf.sub_heading("E.2", "Backup Requirements")
    pdf.body(
        "The following backup schedule shall be maintained:\n\n"
        "  Database: Automated snapshots every 6 hours, retained for 30 days.\n"
        "  Application code: Stored in version control; deployed via CI/CD.\n"
        "  User-generated content: Daily incremental backups, weekly full "
        "backups, retained for 90 days.\n"
        "  Configuration: Infrastructure-as-code stored in version control.\n"
        "  Logs: Centralized log aggregation with 12-month retention.\n\n"
        "All backups shall be encrypted at rest using AES-256 and stored "
        "in a geographically separate AWS region from the primary deployment."
    )

    pdf.sub_heading("E.3", "Failover Architecture")
    pdf.body(
        "The production architecture shall include:\n\n"
        "(a) Multi-AZ deployment for all stateful services (databases, "
        "caches, message queues).\n\n"
        "(b) Auto-scaling groups for application tier with minimum "
        "capacity of 2 instances across separate availability zones.\n\n"
        "(c) Route 53 health checks with automated DNS failover for "
        "public-facing endpoints.\n\n"
        "(d) Read replicas for database services to handle read traffic "
        "during primary instance maintenance or failure.\n\n"
        "(e) CloudFront CDN for static content with origin failover "
        "configuration."
    )

    pdf.sub_heading("E.4", "Testing Requirements")
    pdf.body(
        "Disaster recovery procedures shall be tested as follows:\n\n"
        "(a) Quarterly: Backup restoration test -- verify that backups "
        "can be restored to a functional state within RPO/RTO targets.\n\n"
        "(b) Semi-annually: Failover test -- simulate AZ failure and "
        "verify automated failover meets RTO.\n\n"
        "(c) Annually: Full DR exercise -- simulate complete region "
        "failure and execute manual recovery procedures.\n\n"
        "Test results shall be documented and shared with Client within "
        "five (5) business days of each test."
    )

    pdf.sub_heading("E.5", "Communication Plan")
    pdf.body(
        "In the event of a service disruption, Consultant shall:\n\n"
        "(a) Notify Client's designated contact within thirty (30) minutes "
        "of detecting a service-impacting incident.\n\n"
        "(b) Provide status updates every sixty (60) minutes during active "
        "incidents.\n\n"
        "(c) Provide a post-incident report within three (3) business days "
        "of incident resolution, including root cause analysis, timeline "
        "of events, impact assessment, and remediation steps."
    )
    pdf.divider()


def exhibit_f(pdf: ContractPDF):
    """Governance and escalation procedures."""
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "EXHIBIT F", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 8, "GOVERNANCE AND ESCALATION PROCEDURES", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(8)
    pdf.divider()

    pdf.sub_heading("F.1", "Project Governance Structure")
    pdf.body(
        "The following governance structure shall apply to all work "
        "performed under this Agreement:\n\n"
        "  Steering Committee: Meets quarterly; composed of senior "
        "leadership from both Parties; responsible for strategic direction, "
        "budget approval, and resolution of escalated issues.\n\n"
        "  Project Management Office: Meets bi-weekly; composed of project "
        "managers from both Parties; responsible for day-to-day oversight, "
        "schedule management, and risk tracking.\n\n"
        "  Technical Working Group: Meets weekly; composed of technical "
        "leads from both Parties; responsible for architecture decisions, "
        "technical standards, and implementation reviews."
    )

    pdf.sub_heading("F.2", "Reporting Requirements")
    pdf.body(
        "Consultant shall provide the following reports:\n\n"
        "  Weekly Status Report: Progress against milestones, work "
        "completed, upcoming activities, risks and issues, resource "
        "utilization. Due each Friday by 5:00 PM Eastern Time.\n\n"
        "  Monthly Executive Summary: High-level progress overview, "
        "budget status, key decisions needed, strategic recommendations. "
        "Due within five (5) business days of month-end.\n\n"
        "  Milestone Completion Report: Detailed documentation of "
        "deliverables produced, acceptance criteria met, lessons learned, "
        "and recommendations for subsequent phases."
    )

    pdf.sub_heading("F.3", "Escalation Matrix")
    pdf.body(
        "Issues shall be escalated according to the following matrix:\n\n"
        "  Level 1 (Working Level): Technical or operational issues "
        "resolved by the assigned team. Target resolution: 2 business "
        "days.\n\n"
        "  Level 2 (Project Management): Issues unresolved at Level 1, "
        "or issues requiring schedule/budget adjustments. Escalated to "
        "project managers. Target resolution: 5 business days.\n\n"
        "  Level 3 (Senior Management): Issues unresolved at Level 2, "
        "or issues with significant business impact. Escalated to "
        "Steering Committee members. Target resolution: 10 business "
        "days.\n\n"
        "  Level 4 (Executive): Issues unresolved at Level 3, or "
        "disputes requiring executive intervention. Escalated to CEO "
        "(Client) and CTO (Consultant). Target resolution: 15 business "
        "days."
    )

    pdf.sub_heading("F.4", "Change Control Board")
    pdf.body(
        "A Change Control Board (CCB) shall be established to review "
        "and approve all proposed changes to scope, schedule, or budget. "
        "The CCB shall consist of one representative from each Party, "
        "with authority to approve changes up to 10% of the applicable "
        "SOW value. Changes exceeding this threshold require Steering "
        "Committee approval.\n\n"
        "The CCB shall meet as needed, with a maximum response time of "
        "five (5) business days from submission of a Change Order request."
    )

    pdf.sub_heading("F.5", "Quality Assurance")
    pdf.body(
        "Consultant shall maintain a quality assurance program that "
        "includes:\n\n"
        "(a) Code review requirements: All code changes shall be reviewed "
        "by at least one peer before merging to the main branch.\n\n"
        "(b) Automated testing: Unit test coverage of at least 80% for "
        "new code; integration tests for all critical paths.\n\n"
        "(c) Static analysis: Automated code quality scanning with no "
        "critical or high-severity findings at deployment.\n\n"
        "(d) Security scanning: Dependency vulnerability scanning and "
        "SAST on every build; DAST quarterly against staging environment.\n\n"
        "(e) Performance testing: Load testing against defined baselines "
        "before each production release."
    )

    pdf.sub_heading("F.6", "Knowledge Management")
    pdf.body(
        "Consultant shall maintain project documentation in a shared "
        "repository accessible to both Parties, including:\n\n"
        "(a) Architecture decision records (ADRs) for all significant "
        "technical decisions.\n\n"
        "(b) Runbooks for operational procedures, deployment, and "
        "troubleshooting.\n\n"
        "(c) API documentation, automatically generated from source code "
        "where possible.\n\n"
        "(d) User guides and training materials for Client Personnel.\n\n"
        "All documentation shall be maintained in Markdown format and "
        "version-controlled alongside the source code."
    )
    pdf.divider()


def exhibit_g(pdf: ContractPDF):
    """AWS infrastructure specifications."""
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "EXHIBIT G", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 8, "TECHNICAL SPECIFICATIONS -- AWS INFRASTRUCTURE", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(8)
    pdf.divider()

    pdf.sub_heading("G.1", "Compute Environment")
    pdf.body(
        "The production environment shall be deployed on the following "
        "AWS infrastructure:\n\n"
        "  Application Tier:\n"
        "    Instance Type: m6i.xlarge (4 vCPU, 16 GiB RAM)\n"
        "    Minimum Instances: 2 (across 2 AZs)\n"
        "    Maximum Instances: 8 (auto-scaling)\n"
        "    Operating System: Amazon Linux 2023\n"
        "    Container Runtime: Amazon ECS on Fargate\n\n"
        "  Database Tier:\n"
        "    Engine: Amazon Aurora PostgreSQL 15.x\n"
        "    Instance Class: db.r6g.xlarge\n"
        "    Multi-AZ: Yes (1 writer, 2 readers)\n"
        "    Storage: Aurora I/O-Optimized, encrypted\n\n"
        "  Cache Tier:\n"
        "    Engine: Amazon ElastiCache for Redis 7.x\n"
        "    Node Type: cache.r6g.large\n"
        "    Cluster Mode: Enabled (3 shards, 2 replicas)\n\n"
        "  Search Tier:\n"
        "    Engine: Amazon OpenSearch Service 2.x\n"
        "    Instance Type: r6g.large.search\n"
        "    Nodes: 3 (dedicated master + 2 data)\n"
        "    Storage: 500 GiB gp3 per data node"
    )

    pdf.sub_heading("G.2", "Networking")
    pdf.body(
        "VPC Configuration:\n"
        "  CIDR: 10.0.0.0/16\n"
        "  Public Subnets: 10.0.1.0/24, 10.0.2.0/24 (2 AZs)\n"
        "  Private Subnets: 10.0.10.0/24, 10.0.20.0/24 (2 AZs)\n"
        "  Database Subnets: 10.0.100.0/24, 10.0.200.0/24 (2 AZs)\n\n"
        "Load Balancing:\n"
        "  Type: Application Load Balancer (ALB)\n"
        "  SSL Termination: ACM-managed certificates\n"
        "  WAF: AWS WAF v2 with OWASP Top 10 rule set\n\n"
        "DNS:\n"
        "  Primary: Amazon Route 53\n"
        "  Domains: larpsy.gold, larpsalot.party, api.larpsalot.party\n"
        "  Health Checks: HTTP/HTTPS with 30-second intervals\n\n"
        "CDN:\n"
        "  Service: Amazon CloudFront\n"
        "  Origins: ALB (dynamic), S3 (static assets)\n"
        "  Cache Policy: Optimized for TTL with query string forwarding\n"
        "  Price Class: PriceClass_100 (US, Canada, Europe)"
    )

    pdf.sub_heading("G.3", "Storage")
    pdf.body(
        "Object Storage:\n"
        "  Service: Amazon S3\n"
        "  Buckets: media assets, user uploads, backups, logs\n"
        "  Versioning: Enabled for media and user uploads\n"
        "  Lifecycle: Transition to S3-IA after 90 days, Glacier after "
        "365 days\n"
        "  Replication: Cross-region replication to us-west-2\n\n"
        "Block Storage:\n"
        "  Type: gp3\n"
        "  IOPS: 3000 (baseline), up to 16000 (provisioned)\n"
        "  Throughput: 125 MiB/s (baseline)\n\n"
        "File Storage:\n"
        "  Service: Amazon EFS\n"
        "  Performance Mode: General Purpose\n"
        "  Throughput Mode: Elastic\n"
        "  Use Case: Shared application configuration and templates"
    )

    pdf.sub_heading("G.4", "CI/CD Pipeline")
    pdf.body(
        "The deployment pipeline shall consist of:\n\n"
        "(a) Source: AWS CodeCommit or GitHub (Client's preference)\n\n"
        "(b) Build: AWS CodeBuild with custom build images\n"
        "    - Unit tests, linting, SAST scanning\n"
        "    - Container image build and push to ECR\n"
        "    - Infrastructure validation (cfn-lint, checkov)\n\n"
        "(c) Deploy: AWS CodeDeploy with blue/green deployment strategy\n"
        "    - Automatic rollback on CloudWatch alarm triggers\n"
        "    - Canary traffic shifting (10% for 5 minutes, then 100%)\n\n"
        "(d) Environments: dev, staging, production\n"
        "    - dev: auto-deploy on merge to develop branch\n"
        "    - staging: auto-deploy on merge to main branch\n"
        "    - production: manual approval gate after staging validation"
    )

    pdf.sub_heading("G.5", "Monitoring and Observability")
    pdf.body(
        "The following monitoring stack shall be implemented:\n\n"
        "  Metrics: Amazon CloudWatch with custom dashboards\n"
        "    - Application: response time, error rate, throughput\n"
        "    - Infrastructure: CPU, memory, disk, network\n"
        "    - Business: active users, content views, search queries\n\n"
        "  Logging: CloudWatch Logs with structured JSON logging\n"
        "    - Centralized log aggregation across all services\n"
        "    - Log Insights queries for troubleshooting\n"
        "    - Retention: 90 days hot, 365 days archived to S3\n\n"
        "  Tracing: AWS X-Ray for distributed tracing\n"
        "    - Sampling rate: 5% in production, 100% in staging\n\n"
        "  Alerting: CloudWatch Alarms with SNS notifications\n"
        "    - PagerDuty integration for critical alerts\n"
        "    - Slack integration for warning-level alerts\n"
        "    - Weekly alert summary reports"
    )

    pdf.sub_heading("G.6", "Cost Estimates")
    pdf.body(
        "Estimated monthly AWS costs (production environment):\n\n"
        "  Compute (ECS Fargate):              $1,200\n"
        "  Database (Aurora PostgreSQL):        $1,800\n"
        "  Cache (ElastiCache Redis):           $  600\n"
        "  Search (OpenSearch):                 $  900\n"
        "  Storage (S3 + EFS + EBS):            $  400\n"
        "  Networking (ALB + CloudFront + NAT):  $  500\n"
        "  Monitoring (CloudWatch + X-Ray):     $  200\n"
        "  Other (KMS, Secrets Manager, etc.):  $  150\n"
        "  ----------------------------------------\n"
        "  Estimated Monthly Total:             $5,750\n"
        "  Estimated Annual Total:              $69,000\n\n"
        "Note: Estimates based on anticipated usage patterns. Actual "
        "costs may vary based on traffic volumes and data growth. "
        "Reserved Instance pricing could reduce compute and database "
        "costs by approximately 30-40%."
    )
    pdf.divider()


def exhibit_h(pdf: ContractPDF):
    """Compliance and regulatory requirements."""
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "EXHIBIT H", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 8, "COMPLIANCE AND REGULATORY REQUIREMENTS", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(8)
    pdf.divider()

    pdf.sub_heading("H.1", "Applicable Regulations")
    pdf.body(
        "Consultant acknowledges that Client's business is subject to the "
        "following regulatory frameworks, and shall ensure that all "
        "Deliverables and services comply with applicable requirements:\n\n"
        "(a) General Data Protection Regulation (GDPR): Client serves "
        "customers in the European Economic Area. All personal data "
        "processing must comply with GDPR requirements, including lawful "
        "basis for processing, data subject rights, data protection impact "
        "assessments, and cross-border transfer mechanisms.\n\n"
        "(b) California Consumer Privacy Act (CCPA/CPRA): Client serves "
        "California residents. Systems must support consumer rights "
        "requests including right to know, right to delete, right to "
        "opt-out of sale, and right to limit use of sensitive information.\n\n"
        "(c) Children's Online Privacy Protection Act (COPPA): Client's "
        "content may be accessed by users under 13. Systems must implement "
        "appropriate age verification and parental consent mechanisms.\n\n"
        "(d) Payment Card Industry Data Security Standard (PCI DSS): "
        "If payment processing is within scope, systems must comply with "
        "PCI DSS Level 2 requirements.\n\n"
        "(e) Americans with Disabilities Act (ADA) / Web Content "
        "Accessibility Guidelines (WCAG): All public-facing web properties "
        "must meet WCAG 2.1 Level AA compliance."
    )

    pdf.sub_heading("H.2", "Privacy by Design")
    pdf.body(
        "Consultant shall implement privacy by design principles in all "
        "Deliverables, including:\n\n"
        "(a) Data minimization: Collect only the minimum personal data "
        "necessary for stated purposes.\n\n"
        "(b) Purpose limitation: Personal data shall be processed only "
        "for specified, explicit, and legitimate purposes.\n\n"
        "(c) Storage limitation: Personal data shall be retained only "
        "for as long as necessary. Automated deletion/anonymization "
        "shall be implemented for expired data.\n\n"
        "(d) Privacy controls: Users shall have accessible controls to "
        "manage their privacy preferences, including consent management, "
        "data export, and account deletion.\n\n"
        "(e) Transparency: Clear, plain-language privacy notices shall "
        "be integrated into all user-facing interfaces."
    )

    pdf.sub_heading("H.3", "Accessibility Requirements")
    pdf.body(
        "All user-facing Deliverables shall meet WCAG 2.1 Level AA, "
        "including but not limited to:\n\n"
        "(a) Perceivable: Text alternatives for non-text content, "
        "captions for multimedia, adaptable layouts, and sufficient "
        "color contrast (4.5:1 for normal text, 3:1 for large text).\n\n"
        "(b) Operable: Full keyboard accessibility, adequate time limits, "
        "no seizure-inducing content, clear navigation mechanisms, and "
        "pointer gesture alternatives.\n\n"
        "(c) Understandable: Readable content, predictable interface "
        "behavior, and input assistance for forms.\n\n"
        "(d) Robust: Compatible with current and foreseeable assistive "
        "technologies, valid HTML markup, and ARIA attributes where "
        "appropriate.\n\n"
        "Consultant shall conduct automated accessibility testing as "
        "part of the CI/CD pipeline and manual accessibility audits "
        "at each major milestone."
    )

    pdf.sub_heading("H.4", "Export Control")
    pdf.body(
        "Client's content may include materials subject to export "
        "control regulations. Consultant shall:\n\n"
        "(a) Not export or re-export any Client data or Deliverables "
        "to sanctioned countries, entities, or individuals.\n\n"
        "(b) Implement appropriate geo-blocking controls as directed "
        "by Client.\n\n"
        "(c) Maintain awareness of applicable export control "
        "regulations (EAR, ITAR) and notify Client of any potential "
        "compliance concerns.\n\n"
        "(d) Ensure that no open-source components incorporated into "
        "Deliverables are subject to export restrictions that would "
        "limit Client's use."
    )

    pdf.sub_heading("H.5", "Audit and Certification")
    pdf.body(
        "Consultant shall:\n\n"
        "(a) Maintain SOC 2 Type II certification throughout the term "
        "of this Agreement, or obtain such certification within twelve "
        "(12) months of the Effective Date.\n\n"
        "(b) Provide copies of audit reports and certifications to "
        "Client upon request.\n\n"
        "(c) Cooperate with Client's compliance audits and regulatory "
        "examinations, providing access to relevant documentation, "
        "systems, and Personnel as needed.\n\n"
        "(d) Promptly notify Client of any material findings from "
        "internal or external audits that may affect Client's "
        "compliance posture."
    )

    pdf.sub_heading("H.6", "Regulatory Change Management")
    pdf.body(
        "Consultant shall monitor relevant regulatory developments "
        "and notify Client of any changes that may affect the "
        "Deliverables or services. Upon mutual agreement, the Parties "
        "shall execute Change Orders as necessary to maintain "
        "regulatory compliance. The cost of compliance-related changes "
        "shall be borne by Client unless such changes result from "
        "Consultant's failure to comply with regulations known at "
        "the time of SOW execution."
    )
    pdf.divider()


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def build_contract(output_path: str):
    pdf = ContractPDF()
    pdf.alias_nb_pages()

    cover_page(pdf)
    table_of_contents(pdf)
    preamble(pdf)
    sec_definitions(pdf)
    sec_scope(pdf)
    sec_fees(pdf)
    sec_ip(pdf)
    sec_confidentiality(pdf)
    sec_noncompete(pdf)
    sec_warranties(pdf)
    sec_indemnification(pdf)
    sec_liability(pdf)
    sec_term(pdf)
    sec_insurance(pdf)
    sec_staffing(pdf)
    sec_data(pdf)
    sec_audit(pdf)
    sec_change_management(pdf)
    sec_acceptance(pdf)
    sec_transition(pdf)
    sec_general(pdf)
    signatures(pdf)
    exhibit_a(pdf)
    exhibit_b(pdf)
    exhibit_c(pdf)
    exhibit_d(pdf)
    exhibit_e(pdf)
    exhibit_f(pdf)
    exhibit_g(pdf)
    exhibit_h(pdf)

    pdf.output(output_path)
    pages = pdf.pages_count
    print(f"Generated {pages}-page contract: {output_path}")
    return pages


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "contracts/bigco-msa.pdf"
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    build_contract(out)
