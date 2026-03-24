import { useState } from "react";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, LineChart, Line, ReferenceLine, Cell } from "recharts";

const CONTEXT_LIMIT = 200000;
const OUTPUT_LIMIT = 8192;

// Tool calls made during naive analysis with approximate token counts
const toolCalls = [
  { step: 1, label: "ls uploads/workspace", inputAdd: 50, outputAdd: 60, cumInput: 13050, cumOutput: 60, note: "Initial file discovery" },
  { step: 2, label: "unzip -l (list contents)", inputAdd: 80, outputAdd: 220, cumInput: 13350, cumOutput: 280, note: "18 files identified, 9.3 MB total" },
  { step: 3, label: "unzip (extract all)", inputAdd: 90, outputAdd: 280, cumInput: 13520, cumOutput: 560, note: "Files extracted to working dir" },
  { step: 4, label: "pdftotext (extract RFP)", inputAdd: 100, outputAdd: 80, cumInput: 13700, cumOutput: 640, note: "77KB text, 11,239 words extracted" },
  { step: 5, label: "pip + doc extraction", inputAdd: 350, outputAdd: 3200, cumInput: 14150, cumOutput: 3840, note: "Addenda + sample contract read" },
  { step: 6, label: "RFP lines 1-200", inputAdd: 120, outputAdd: 3100, cumInput: 14390, cumOutput: 6940, note: "ToC, intro, definitions, scope summary" },
  { step: 7, label: "RFP lines 200-500", inputAdd: 120, outputAdd: 3400, cumInput: 14630, cumOutput: 10340, note: "Scopes A-I detailed requirements" },
  { step: 8, label: "RFP lines 500-900", inputAdd: 120, outputAdd: 4200, cumInput: 14870, cumOutput: 14540, note: "Process rules, milestones, MWBE" },
  { step: 9, label: "RFP lines 900-1200", inputAdd: 120, outputAdd: 4100, cumInput: 15110, cumOutput: 18640, note: "IVOSB, ADA, compliance, proposal prep" },
  { step: 10, label: "RFP lines 1200-1844", inputAdd: 120, outputAdd: 500, cumInput: 15350, cumOutput: 19140, note: "⚠️ HIT OUTPUT LIMIT — persisted to disk" },
  { step: 11, label: "Read persisted file", inputAdd: 4000, outputAdd: 3800, cumInput: 19470, cumOutput: 22940, note: "Business proposal, eval criteria" },
  { step: 12, label: "catdoc addenda (failed)", inputAdd: 80, outputAdd: 50, cumInput: 19630, cumOutput: 22990, note: "catdoc not available" },
  { step: 13, label: "strings + docx extraction", inputAdd: 300, outputAdd: 3600, cumInput: 20050, cumOutput: 26590, note: "Addenda & contract read; XML noise" },
  { step: 14, label: "File size analysis", inputAdd: 280, outputAdd: 480, cumInput: 20450, cumOutput: 27070, note: "Token estimates for unread files" },
];

// Files in the RFP package with their estimated tokens if read
const fileData = [
  { name: "020attJ.pdf\n(Tax Forms)", tokens: 339506, read: false, critical: true, category: "Forms" },
  { name: "RFP Main\n(PDF binary)", tokens: 49316, read: false, note: "used txt", category: "Core" },
  { name: "020attH.pdf\n(Filing Process)", tokens: 18726, read: false, critical: true, category: "Process" },
  { name: "020attI.pdf\n(Agent Process)", tokens: 16303, read: false, critical: true, category: "Process" },
  { name: "rfp_main.txt\n(extracted)", tokens: 19326, read: true, category: "Core" },
  { name: "020attE.doc\n(Biz Template)", tokens: 4147, read: false, category: "Template" },
  { name: "020attB.docx\n(Sample Contract)", tokens: 3271, read: true, partial: true, category: "Contract" },
  { name: "020add1.doc\n(Addendum 1)", tokens: 2553, read: true, partial: true, category: "Amendment" },
  { name: "020add2.doc\n(Addendum 2)", tokens: 2592, read: true, partial: true, category: "Amendment" },
  { name: "020attC.xls\n(Econ Impact)", tokens: 2566, read: false, category: "Template" },
  { name: "020attA.docx\n(MWBE Form)", tokens: 1393, read: false, category: "Compliance" },
  { name: "020attA1.docx\n(IVOSB Form)", tokens: 1387, read: false, category: "Compliance" },
  { name: "020attF.docx\n(Tech Proposal)", tokens: 1543, read: true, partial: true, category: "Template" },
  { name: "020attD.xlsx\n(Cost Template)", tokens: 717, read: false, category: "Template" },
  { name: "Q&A attG.xlsx", tokens: 543, read: false, category: "QA" },
  { name: "020attG.xlsx\n(Q&A Template)", tokens: 394, read: false, category: "QA" },
  { name: "020attG Resp.xlsx", tokens: 526, read: false, category: "Template" },
  { name: "020attK.xlsx\n(Ref Check)", tokens: 280, read: false, category: "Template" },
];

const issues = [
  { category: "Scope", severity: "High", title: "Deferred Scope in Notifications/Reports", detail: "Scope F explicitly states 'Additional details will be provided during the planning stage' for both notifications AND reporting requirements. This is undefined work the vendor must price blind." },
  { category: "Scope", severity: "High", title: "Vague Quality Standards", detail: "System must be 'user-friendly, expansive, and sophisticated' — no measurable acceptance criteria, no SLAs, no uptime targets, no security framework specified (NIST? StateRAMP?)." },
  { category: "Scope", severity: "High", title: "92-County CAMA Integration Complexity", detail: "REST API integration with County Assessor CAMA software systems across all 92 Indiana counties. CAMA vendors are not specified; REST API standards are not defined. Enormous integration risk." },
  { category: "Timeline", severity: "High", title: "Aggressive Jan 1, 2021 Target", detail: "RFP issued June 24, 2019; proposals due Aug 14 (after extension). Award ~Sept 2019. That leaves ~15 months for a multi-county, multi-form, statewide system. Respondents are asked to provide TWO timelines — aggressive AND less aggressive — signaling the State itself doubts feasibility." },
  { category: "Timeline", severity: "Medium", title: "Two Addenda Already Issued", detail: "Addendum 1 extended the deadline by 2 weeks (July 31 → Aug 14). Addendum 2 updated the Cost Proposal template. Both issued before proposals were due, suggesting the RFP was not fully baked at release." },
  { category: "Contract", severity: "High", title: "Funding Cancellation Clause is Mandatory", detail: "The State can cancel the contract for funding reasons — this is a non-negotiable mandatory clause. For a multi-year, multi-million dollar system build, this creates existential financial risk for the vendor." },
  { category: "Contract", severity: "High", title: "State Owns All Work Product", detail: "Ownership of Documents and Materials is a mandatory clause. All IP, code, and deliverables transfer to the State. No carve-outs for vendor's pre-existing IP or platform are visible in the sample contract." },
  { category: "Contract", severity: "Medium", title: "Entire Proposal Can Become Contract", detail: "Section 2.3.5: 'Any or all portions of this RFP and any or all portions of the Respondents response may be incorporated as part of the final contract.' Vendors must be very careful what they put in their proposals." },
  { category: "Financial", severity: "High", title: "$300K Financial Responsibility Bond Required", detail: "Must be delivered BEFORE the contract becomes effective. Irrevocable letter of credit, certified check, cashier's check, or surety bond. This is a significant barrier to smaller/newer vendors." },
  { category: "Financial", severity: "Medium", title: "180-Day Firm Pricing Requirement", detail: "All pricing must remain firm and open for 180 days from proposal due date. No escalation clauses permitted. For a contract covering multiple years of potential scope changes, this is risky." },
  { category: "Compliance", severity: "Medium", title: "MWBE/IVOSB Requirements Are Complex", detail: "8% MBE + 8% WBE + 3% IVOSB subcontractor commitments required. Must use certified Indiana firms from IDOA directory. Monthly Pay Audit reporting. Subcontract copies due within 30 days. Failure = potential material breach." },
  { category: "Evaluation", severity: "Medium", title: "Opaque Technical Scoring", detail: "The evaluation section lists Pass/Fail, Management/Quality, Cost, Buy Indiana (5pts), MWBE (10pts), IVOSB (5pts) — but never states what the total point value is for the Technical Proposal vs. Business Proposal. The relative weight of technical quality is unclear." },
  { category: "Evaluation", severity: "Low", title: "CD-ROM Submission Required", detail: "In 2019, the RFP required proposals on CD-ROM (one original + three copies). Physical delivery with weapons screening at Indiana Government Center. This creates logistical friction and is already technically outdated at time of issue." },
  { category: "Scope", severity: "Medium", title: "Amendment Limits Are Restrictive", detail: "Only ONE amendment allowed per filing (Scope D). Given the State retains the right to expand scope post-award, this creates a maintenance burden where one mistake by a filer forfeits their amendment right forever." },
  { category: "Scope", severity: "Medium", title: "Document Retention Policy Is Undefined", detail: "Scope E requires storage 'in accordance to the State's retention policies' — but those policies are not included in the RFP or attachments. Vendors cannot properly architect or price storage without this." },
];

const SEVERITY_COLORS = { High: "#ef4444", Medium: "#f97316", Low: "#eab308" };
const CATEGORY_COLORS = {
  Core: "#6366f1", Forms: "#ec4899", Process: "#8b5cf6",
  Contract: "#ef4444", Amendment: "#f97316", Compliance: "#14b8a6",
  Template: "#94a3b8", QA: "#64748b"
};

export default function RFPAnalysis() {
  const [activeTab, setActiveTab] = useState("issues");
  const [selectedIssue, setSelectedIssue] = useState(null);

  const contextData = toolCalls.map(t => ({
    step: `Step ${t.step}`,
    label: t.label,
    "Input Tokens": t.cumInput,
    "Output Tokens": t.cumOutput,
    note: t.note,
  }));

  const fileChartData = fileData
    .sort((a, b) => b.tokens - a.tokens)
    .map(f => ({
      name: f.name.replace(/\n/g, " "),
      tokens: f.tokens,
      read: f.read,
      partial: f.partial,
      critical: f.critical,
      category: f.category,
    }));

  const totalReadTokens = fileData.filter(f => f.read).reduce((s, f) => s + f.tokens, 0);
  const totalUnreadTokens = fileData.filter(f => !f.read).reduce((s, f) => s + f.tokens, 0);
  const totalIfAll = totalReadTokens + totalUnreadTokens;

  const issuesBySeverity = {
    High: issues.filter(i => i.severity === "High").length,
    Medium: issues.filter(i => i.severity === "Medium").length,
    Low: issues.filter(i => i.severity === "Low").length,
  };

  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      const step = toolCalls.find(t => `Step ${t.step}` === label);
      return (
        <div style={{background:"#1e293b",border:"1px solid #334155",padding:"12px",borderRadius:"8px",maxWidth:"280px"}}>
          <p style={{color:"#94a3b8",fontSize:"11px",margin:"0 0 4px"}}>{label}</p>
          <p style={{color:"#e2e8f0",fontWeight:"bold",fontSize:"12px",margin:"0 0 8px"}}>{step?.label}</p>
          {payload.map(p => (
            <p key={p.name} style={{color:p.color,fontSize:"12px",margin:"2px 0"}}>
              {p.name}: {p.value.toLocaleString()} tokens
            </p>
          ))}
          {step?.note && <p style={{color:"#94a3b8",fontSize:"11px",margin:"8px 0 0",fontStyle:"italic"}}>{step.note}</p>}
        </div>
      );
    }
    return null;
  };

  return (
    <div style={{fontFamily:"system-ui,sans-serif",background:"#0f172a",color:"#e2e8f0",minHeight:"100vh",padding:"24px"}}>
      {/* Header */}
      <div style={{marginBottom:"24px"}}>
        <div style={{display:"flex",alignItems:"center",gap:"12px",marginBottom:"8px"}}>
          <div style={{background:"#dc2626",borderRadius:"8px",padding:"8px 14px",fontSize:"12px",fontWeight:"700",letterSpacing:"0.05em"}}>
            RFP 20-020
          </div>
          <div>
            <h1 style={{margin:0,fontSize:"20px",fontWeight:"700",color:"#f1f5f9"}}>
              Indiana Dept. of Administration — Personal Property Tax Online Filing System
            </h1>
            <p style={{margin:"4px 0 0",fontSize:"13px",color:"#64748b"}}>
              Naive Context-Buffer Analysis · {issues.length} Issues Identified · {fileData.length} Files in Package
            </p>
          </div>
        </div>

        {/* Summary cards */}
        <div style={{display:"grid",gridTemplateColumns:"repeat(4,1fr)",gap:"12px",marginTop:"16px"}}>
          {[
            { label: "High Severity Issues", value: issuesBySeverity.High, color: "#ef4444", bg: "#1f0a0a" },
            { label: "Medium Severity Issues", value: issuesBySeverity.Medium, color: "#f97316", bg: "#1a0d00" },
            { label: "Files NOT Read", value: fileData.filter(f=>!f.read).length + " of " + fileData.length, color: "#f59e0b", bg: "#1a1200" },
            { label: "Tokens Left Unread", value: (totalUnreadTokens/1000).toFixed(0)+"K est.", color: "#a78bfa", bg: "#0d0a1f" },
          ].map(card => (
            <div key={card.label} style={{background:card.bg,border:`1px solid ${card.color}33`,borderRadius:"10px",padding:"14px"}}>
              <div style={{fontSize:"24px",fontWeight:"800",color:card.color}}>{card.value}</div>
              <div style={{fontSize:"12px",color:"#94a3b8",marginTop:"4px"}}>{card.label}</div>
            </div>
          ))}
        </div>
      </div>

      {/* Tabs */}
      <div style={{display:"flex",gap:"8px",marginBottom:"20px",borderBottom:"1px solid #1e293b",paddingBottom:"8px"}}>
        {[["issues","Issues Found"],["tokens","Token Usage"],["files","File Coverage"],["risks","Context Risks"]].map(([id,label]) => (
          <button key={id} onClick={()=>setActiveTab(id)}
            style={{background:activeTab===id?"#6366f1":"transparent",color:activeTab===id?"white":"#94a3b8",
              border:activeTab===id?"none":"1px solid #1e293b",borderRadius:"6px",padding:"7px 16px",
              cursor:"pointer",fontSize:"13px",fontWeight:"500"}}>
            {label}
          </button>
        ))}
      </div>

      {/* ISSUES TAB */}
      {activeTab === "issues" && (
        <div>
          <div style={{display:"grid",gridTemplateColumns:"1fr 1fr",gap:"12px"}}>
            {issues.map((issue, i) => (
              <div key={i}
                onClick={() => setSelectedIssue(selectedIssue === i ? null : i)}
                style={{background:"#1e293b",border:`1px solid ${SEVERITY_COLORS[issue.severity]}44`,
                  borderLeft:`3px solid ${SEVERITY_COLORS[issue.severity]}`,
                  borderRadius:"8px",padding:"14px",cursor:"pointer",
                  transition:"all 0.15s",opacity:1}}>
                <div style={{display:"flex",justifyContent:"space-between",alignItems:"flex-start",marginBottom:"6px"}}>
                  <span style={{background:`${SEVERITY_COLORS[issue.severity]}22`,color:SEVERITY_COLORS[issue.severity],
                    fontSize:"10px",fontWeight:"700",padding:"2px 8px",borderRadius:"4px",letterSpacing:"0.08em"}}>
                    {issue.severity.toUpperCase()}
                  </span>
                  <span style={{fontSize:"10px",color:"#64748b",background:"#0f172a",padding:"2px 8px",borderRadius:"4px"}}>
                    {issue.category}
                  </span>
                </div>
                <h3 style={{margin:"0 0 6px",fontSize:"13px",fontWeight:"600",color:"#f1f5f9"}}>{issue.title}</h3>
                {selectedIssue === i && (
                  <p style={{margin:0,fontSize:"12px",color:"#94a3b8",lineHeight:"1.6"}}>{issue.detail}</p>
                )}
                {selectedIssue !== i && (
                  <p style={{margin:0,fontSize:"11px",color:"#475569",fontStyle:"italic"}}>Click to expand ↓</p>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* TOKEN USAGE TAB */}
      {activeTab === "tokens" && (
        <div>
          <div style={{background:"#1e293b",borderRadius:"10px",padding:"20px",marginBottom:"16px"}}>
            <h2 style={{margin:"0 0 16px",fontSize:"15px",fontWeight:"600",color:"#f1f5f9"}}>
              Cumulative Token Consumption — Step by Step
            </h2>
            <ResponsiveContainer width="100%" height={320}>
              <LineChart data={contextData} margin={{top:5,right:20,left:20,bottom:5}}>
                <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                <XAxis dataKey="step" tick={{fill:"#64748b",fontSize:10}} />
                <YAxis tick={{fill:"#64748b",fontSize:10}} tickFormatter={v=>`${(v/1000).toFixed(0)}K`} />
                <Tooltip content={<CustomTooltip />} />
                <Legend wrapperStyle={{color:"#94a3b8",fontSize:"12px"}} />
                <Line type="monotone" dataKey="Input Tokens" stroke="#6366f1" strokeWidth={2} dot={{fill:"#6366f1",r:4}} />
                <Line type="monotone" dataKey="Output Tokens" stroke="#10b981" strokeWidth={2} dot={{fill:"#10b981",r:4}} />
                <ReferenceLine y={OUTPUT_LIMIT} stroke="#f97316" strokeDasharray="4 4" label={{value:"Output Limit ~8K",fill:"#f97316",fontSize:10,position:"right"}} />
              </LineChart>
            </ResponsiveContainer>
          </div>

          {/* Step-by-step table */}
          <div style={{background:"#1e293b",borderRadius:"10px",padding:"20px"}}>
            <h2 style={{margin:"0 0 14px",fontSize:"15px",fontWeight:"600",color:"#f1f5f9"}}>Tool Call Log</h2>
            <table style={{width:"100%",borderCollapse:"collapse",fontSize:"12px"}}>
              <thead>
                <tr style={{borderBottom:"1px solid #334155"}}>
                  {["Step","Action","Cum. Input","Cum. Output","Note"].map(h=>(
                    <th key={h} style={{textAlign:"left",padding:"8px",color:"#64748b",fontWeight:"600"}}>{h}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {toolCalls.map(t => (
                  <tr key={t.step} style={{borderBottom:"1px solid #0f172a",background:t.step===10?"#1f0a0a":"transparent"}}>
                    <td style={{padding:"8px",color:"#64748b"}}>{t.step}</td>
                    <td style={{padding:"8px",color:"#e2e8f0",fontWeight:t.step===10?"700":"400"}}>
                      {t.label}
                      {t.step===10 && <span style={{color:"#f97316",marginLeft:"6px",fontSize:"10px"}}>⚠️ OUTPUT LIMIT HIT</span>}
                    </td>
                    <td style={{padding:"8px",color:"#a78bfa"}}>{t.cumInput.toLocaleString()}</td>
                    <td style={{padding:"8px",color:"#34d399"}}>{t.cumOutput.toLocaleString()}</td>
                    <td style={{padding:"8px",color:"#64748b",fontStyle:"italic"}}>{t.note}</td>
                  </tr>
                ))}
              </tbody>
            </table>
            <p style={{margin:"12px 0 0",fontSize:"11px",color:"#475569",fontStyle:"italic"}}>
              Note: Token counts are estimates. Actual counts vary by model tokenization. System prompt (~12K tokens) not shown. Input tokens accumulate as conversation grows.
            </p>
          </div>
        </div>
      )}

      {/* FILE COVERAGE TAB */}
      {activeTab === "files" && (
        <div>
          <div style={{background:"#1e293b",borderRadius:"10px",padding:"20px",marginBottom:"16px"}}>
            <h2 style={{margin:"0 0 6px",fontSize:"15px",fontWeight:"600",color:"#f1f5f9"}}>File Token Estimates vs. What Was Read</h2>
            <p style={{margin:"0 0 16px",fontSize:"12px",color:"#64748b"}}>
              Total estimated tokens if all files read: <strong style={{color:"#a78bfa"}}>{(totalIfAll/1000).toFixed(0)}K</strong> |
              Actually read: <strong style={{color:"#10b981"}}>{(totalReadTokens/1000).toFixed(0)}K</strong> |
              Unread: <strong style={{color:"#ef4444"}}>{(totalUnreadTokens/1000).toFixed(0)}K</strong>
            </p>
            <ResponsiveContainer width="100%" height={360}>
              <BarChart data={fileChartData} margin={{top:5,right:20,left:20,bottom:80}}>
                <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                <XAxis dataKey="name" tick={{fill:"#64748b",fontSize:9}} angle={-35} textAnchor="end" height={90} />
                <YAxis tick={{fill:"#64748b",fontSize:10}} tickFormatter={v=>`${(v/1000).toFixed(0)}K`} />
                <Tooltip formatter={(v,n,p)=>[`${v.toLocaleString()} tokens (${p.payload.read?p.payload.partial?"Partially read":"Read":"NOT read"})`,p.payload.category]} />
                <Bar dataKey="tokens" radius={[4,4,0,0]}>
                  {fileChartData.map((entry, i) => (
                    <Cell key={i}
                      fill={entry.read ? (entry.partial ? "#f59e0b" : "#10b981") : (entry.critical ? "#ef4444" : "#475569")}
                    />
                  ))}
                </Bar>
                <ReferenceLine y={CONTEXT_LIMIT} stroke="#6366f1" strokeDasharray="4 4" label={{value:"200K Context Limit",fill:"#6366f1",fontSize:10}} />
              </BarChart>
            </ResponsiveContainer>
            <div style={{display:"flex",gap:"16px",marginTop:"8px",justifyContent:"center"}}>
              {[["#10b981","Fully Read"],["#f59e0b","Partially Read (XML noise)"],["#ef4444","Unread – Critical"],["#475569","Unread – Supporting"]].map(([color,label])=>(
                <div key={label} style={{display:"flex",alignItems:"center",gap:"6px",fontSize:"11px",color:"#94a3b8"}}>
                  <div style={{width:"12px",height:"12px",background:color,borderRadius:"2px"}}/>
                  {label}
                </div>
              ))}
            </div>
          </div>

          <div style={{background:"#1f0a0a",border:"1px solid #ef444444",borderRadius:"10px",padding:"16px"}}>
            <h3 style={{margin:"0 0 10px",color:"#ef4444",fontSize:"13px",fontWeight:"700"}}>⚠️ Critical Unread Files</h3>
            {fileData.filter(f=>!f.read && f.critical).map(f=>(
              <div key={f.name} style={{marginBottom:"8px",paddingBottom:"8px",borderBottom:"1px solid #2d1515"}}>
                <span style={{color:"#fca5a5",fontWeight:"600",fontSize:"12px"}}>{f.name.replace(/\n/g," ")}</span>
                <span style={{color:"#64748b",fontSize:"11px",marginLeft:"8px"}}>~{(f.tokens/1000).toFixed(0)}K estimated tokens</span>
                <p style={{margin:"4px 0 0",fontSize:"11px",color:"#94a3b8"}}>
                  {f.name.includes("attJ") && "Contains all 7 personal property tax form definitions (Forms 102, 103-Short, 103-Long, 103-N, 103-O, 104, 106). Critical for understanding actual technical requirements."}
                  {f.name.includes("attH") && "Documents the online filing and transmission process to County Assessors. Critical for understanding the county integration architecture."}
                  {f.name.includes("attI") && "Documents the authorized agent acceptance process. Critical for Scope A delegation requirements."}
                </p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* CONTEXT RISKS TAB */}
      {activeTab === "risks" && (
        <div style={{display:"grid",gridTemplateColumns:"1fr 1fr",gap:"16px"}}>
          {[
            {
              title: "🔴 Token Overflow Risk",
              color: "#ef4444",
              content: `AttJ (tax forms PDF) alone estimates ~340K tokens — more than the entire 200K context window. Even reading just the main RFP + all attachments would require ~430K tokens total, roughly 2.15x the context limit. A naive approach physically cannot hold this entire RFP package in a single context.`
            },
            {
              title: "🟠 Tool Output Truncation",
              color: "#f97316",
              content: `At Step 10, reading lines 1200-1844 of the RFP hit the tool output limit (~8K characters). The system automatically persisted the content to disk and returned a truncated preview. Without noticing this, you could miss the final sections — including evaluation criteria weights and scoring details. This happened silently.`
            },
            {
              title: "🟡 Context Poisoning from Binary Formats",
              color: "#eab308",
              content: `The .doc addenda files (020add1.doc, 020add2.doc) are old binary Word formats. Extracting them with 'strings' returned XML metadata noise alongside the actual content. The substantive text (2 sentences each) was buried in hundreds of lines of SharePoint/OPC XML. Naive extraction wastes tokens on garbage.`
            },
            {
              title: "🟡 Conversation Growth Compounds Cost",
              color: "#eab308",
              content: `Every tool call adds to the input context for the next call. By Step 14, the cumulative input context is ~20K tokens — and this is before writing any analysis. In a full context-buffer approach, the analysis itself then gets re-read in every subsequent turn. Long conversations can exceed limits unexpectedly.`
            },
            {
              title: "🟣 No Retrieval = No Re-Query",
              color: "#a78bfa",
              content: `Without a retrieval layer (e.g., ChromaDB, embeddings), once the RFP text scrolls out of the active context window, it is gone. You cannot ask "what did section 2.3.5 say about contract clauses?" in a later turn without re-reading the file. Every targeted question requires a fresh file read.`
            },
            {
              title: "🟣 Coverage Is Incomplete — Silently",
              color: "#a78bfa",
              content: `This analysis did NOT read: AttJ (7 tax forms — the core technical deliverable), AttH (filing process diagrams), AttI (agent process), AttE (full business proposal template), or AttC/D (cost/economic templates). An analyst relying solely on this naive pass would be missing ~95% of the supporting detail, with no warning that it was skipped.`
            },
            {
              title: "🔵 No Structured Memory",
              color: "#38bdf8",
              content: `Everything discovered in a naive analysis lives only in the conversation context. There's no structured database of clauses, no version tracking, no ability to diff against an addendum, no cross-reference between sections. If the addenda change a requirement, you'd have to re-read both the original and the addendum and reconcile manually.`
            },
            {
              title: "🔵 Skills Approach Would Mitigate Most Risks",
              color: "#38bdf8",
              content: `The document-review skill (load-document + eval-document + search-document) uses SQLite + ChromaDB to persist parsed clauses. This means: (1) token costs are paid once at load time, (2) any section can be retrieved semantically on demand, (3) addenda can be tracked as versioned updates, and (4) analysis scales beyond context limits.`
            },
          ].map(risk => (
            <div key={risk.title} style={{background:"#1e293b",border:`1px solid ${risk.color}33`,borderLeft:`3px solid ${risk.color}`,borderRadius:"8px",padding:"16px"}}>
              <h3 style={{margin:"0 0 10px",fontSize:"13px",fontWeight:"700",color:risk.color}}>{risk.title}</h3>
              <p style={{margin:0,fontSize:"12px",color:"#94a3b8",lineHeight:"1.7"}}>{risk.content}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
