Title: Cyber threat actors: AI-assisted intrusion research

URL Source: https://openai.com/index/disrupting-malicious-uses-of-ai-cyber-threat-actors

Markdown Content:
## Actor

We banned accounts demonstrating activity potentially associated with publicly reported Democratic People’s Republic of Korea (DPRK)-affiliated threat actors. Some of these accounts engaged in activity involving TTPs consistent with a threat group known as [VELVET CHOLLIMA (AKA Kimsuky, Emerald Sleet)⁠(opens in a new window)](https://attack.mitre.org/groups/G0094/), while other accounts were potentially related to an actor that was assessed by a credible source to be linked to [STARDUST CHOLLIMA (AKA APT38, Sapphire Sleet)⁠(opens in a new window)](https://attack.mitre.org/groups/G0082/). We detected these accounts following a tip from a trusted industry partner.

## Behaviour

The banned accounts primarily used our tools to pursue information likely related to cyber intrusion tools or operations. They also demonstrated interest in cryptocurrency-related topics, likely in relation to financially motivated activities. This blend of financial and cyber-related activity is typical for DPRK-associated threat groups.

## Completions

The actors used our models for coding assistance and debugging, along with researching security-related open-source code. This included debugging and development assistance for publicly available tools and code that could be used for Remote Desktop Protocol (RDP) brute force attacks, as well as assistance on the use of open-source Remote Administration Tools (RAT).

While debugging auto-start extensibility point (ASEP) locations and techniques for MacOS, the actor revealed staging URLs for binaries (compiled executable files) that appeared to be unknown to security vendors at the time. We submitted the staging URLs to an online scanning service to facilitate sharing with the security community, and the binaries are now reliably detected by a number of vendors, providing protection for potential victims.

*   Asking about vulnerabilities in various applications: LLM-informed reconnaissance.
*   Developing and troubleshooting a C#-based RDP client to enable brute-force attacks: LLM-Aided Development.
*   Requesting code to bypass security warnings for unauthorized RDP access: LLM-Aided Development.
*   Requesting numerous PowerShell scripts for RDP connections, file upload/download, executing code from memory, and obfuscating HTML content: LLM-Enhanced Scripting Techniques; LLM-Enhanced Anomaly Detection Evasion.
*   Discussing creating and deploying obfuscated payloads for execution: LLM-Optimized Payload Crafting.
*   Seeking methods to conduct targeted phishing and social engineering against cryptocurrency investors and traders, as well as more generic phishing content: LLM-Supported Social Engineering.
*   Crafting phishing emails and notifications to manipulate users into revealing sensitive information: LLM-Supported Social Engineering.
*   Researching open-source Remote Administration Tools (RATs): LLM-Assisted Post-Compromise Activity.

## Impact

Prompts and queries from the actor were primarily based on existing open-source information and the provided model generations either did not offer any novel capability or were refusals to respond. We banned the accounts associated with the threat actor, and shared their payloads with the security community to further disrupt their operations.
