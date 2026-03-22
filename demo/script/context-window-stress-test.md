
**Context Window Stress Test — RFP Analysis (No Optimization)**

I've uploaded an RFP package: `1-RFP 20-020 - Original Documents.zip`

Your job: analyze this RFP and tell me what concerns a consulting company should have before bidding. But you must follow these rules exactly:

**Rules:**
1. Extract the zip and read EVERY document as PDF page images — no text extraction, no `pdftotext`, no python parsers, no OCR-to-string. Use the Read tool on each file directly.
2. For .doc/.docx/.xls/.xlsx files, convert them to PDF first (`libreoffice --headless --convert-to pdf`), then read the resulting PDFs as images.
3. Read pages sequentially in batches of 20. Do NOT skip any pages, even blank ones.
4. Do NOT summarize-as-you-go. Hold everything in context and do your analysis at the end, after all pages have been read.
5. After each batch, report: batch number, cumulative pages read, estimated tokens consumed, estimated % context remaining.
6. When you notice degradation — forgetting earlier document details, conflating sections, vague or generic analysis — call it out explicitly.
7. After reading all documents (or hitting the wall), produce your RFP risk analysis based only on what you can still recall.

**The point of this exercise:** We're demonstrating that naive document ingestion (reading everything as images without chunking, summarization, or text extraction) burns through context catastrophically fast. The RFP has ~17 documents and hundreds of pages. You will not make it through all of them. That's the lesson.

Start by extracting the zip and listing all files with their page counts. Then begin reading.
