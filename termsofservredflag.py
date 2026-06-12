# ------------ project details -------------
# title: terms of service "red flag" scraper
# course: legal tech & compliance (lgl-201)
# author: Werlyne Alphonse
# date: June 12th, 2026
# ------------------------------------------

import re

# — setup —
# list of legal keywords to look out for
red_flags = [
    # original core terms
    "third-party", "arbitration", "class action", "indemnify", "waive",
    
    # data privacy & user tracking
    "opt-out", "tracking", "affiliates", "selling your",
    
    # sneaky financial clauses
    "automatic renewal", "subscription", "recurring", "cancellation fee",
    
    # user rights & ownership
    "perpetual", "royalty-free", "sole discretion", "liquidated damages", "as-is"
]

# — context trimmer —
def trim_context(sentence, flag_word):
    # split sentence into a list of individual words
    words = sentence.split()
    
    # if sentence is short enough, return it completely
    if len(words) <= 20:
        return sentence
        
    # find where the flag word lives in the word list
    target_idx = -1
    for idx in range(len(words)):
        if re.search(flag_word, words[idx], re.IGNORECASE):
            target_idx = idx
            break
            
    # fallback if direct index matching is tricky
    if target_idx == -1:
        return sentence
        
    # calculate safe start and end boundaries for slicing
    start_idx = max(0, target_idx - 11)
    end_idx = min(len(words), target_idx + 10) # +10 to include the word + 9 words after
    
    # extract the specific window of words and join back to a string
    trimmed_words = words[start_idx:end_idx]
    trimmed_text = " ".join(trimmed_words)
    
    return f"... {trimmed_text} ..."

# — scan function —
def scan_tos(text_data, keywords):
    # stores processed strings that contain a red flag
    flagged_outputs = []
    
    # split contract into separate sentences by periods
    sentences = text_data.split(".")
    
    for sentence in sentences:
        clean_sentence = sentence.strip()
        
        # skip empty strings
        if not clean_sentence:
            continue
            
        # check if any flag word appears in current sentence
        for flag in keywords:
            if re.search(flag, clean_sentence, re.IGNORECASE):
                # format output based on sentence word count
                final_display = trim_context(clean_sentence, flag)
                flagged_outputs.append(final_display)
                break 
                
    return flagged_outputs

# — main application loop —
# boolean flag keeps program active until explicit user exit
app_active = True

while app_active:
    # — user interface —
    print("\n====================================================")
    print("      WELCOME TO THE TOS RED FLAG SCRAPER           ")
    print("====================================================")
    print("Summary: This tool scans lengthy Terms of Service   ")
    print("agreements for common predatory clauses, such as    ")
    print("hidden arbitration rules or third-party data sales. ")
    print("====================================================\n")
    
    print("Select an ingestion method:")
    print("1. Copy and Paste text directly")
    print("2. Scrape terms from a website URL")
    
    choice = input("\nEnter choice (1 or 2): ").strip()
    
    user_text = ""
    
    if choice == "2":
        url_input = input("\nEnter the URL to scrape: ").strip()
        print(f"\nAttempting to connect to: {url_input} ...")
        # simulation of scraping restriction / blocking
        print("Error: Automated scraping blocked by site's robots.txt policy.")
        print("Switching alternative input method to manual copy-paste.")
        choice = "1" 
    
    if choice == "1":
        print("\nPlease paste your Terms of Service text below.")
        print("When finished, press Enter twice to execute scanning:")
        
        # collect multi-line paste input from user
        lines = []
        while True:
            line = input()
            if line == "":
                break
            lines.append(line)
        user_text = " ".join(lines)
    
    # — execution & results —
    if user_text.strip():
        found_flags = scan_tos(user_text, red_flags)
        
        print("\n— results —")
        print(f"Total flags detected: {len(found_flags)}")
        print("----------------------------------------------------")
        for item in found_flags:
            print(f"- {item}")
        print("----------------------------------------------------")
    else:
        print("\n— results —")
        print("No usable text was provided for analysis.")
        
    # — loop control prompt —
    print("\nWould you like to scan another document?")
    repeat_choice = input("Enter 'y' for yes, or any other key to exit: ").strip().lower()
    
    if repeat_choice != "y":
        app_active = False
        print("\nThank you for using the ToS Red Flag Scraper. Goodbye!")
        print("\nMade By Werlyne Alphonse | Legal Tech & Compliance (LGL-201) | June 2026")