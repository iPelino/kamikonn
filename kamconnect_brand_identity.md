# KamConnect Brand Identity Guidelines

## 1. Brand Essence
**KamConnect** (*Kaminuza Connect*) is the digital bridge for Rwanda's academic ecosystem. It represents the intersection of formal academia and vibrant youth culture. 

*   **Mission:** To break down campus silos and make academic and community events visible, accessible, and engaging.
*   **Brand Archetype:** The Connector (brings people together) + The Sage (shares knowledge).
*   **Vibe:** Professional yet energetic. Trustworthy yet modern. It should feel like a premium startup, not a boring university administrative portal.

---

## 2. Color Palette
Drawing inspiration from Rwanda's landscape and the energy of student life, the palette balances growth (green) with energy (amber). This perfectly matches the Tailwind setup we saw earlier in your code.

### Primary Colors
*   **Forest Green (HEX: #0F3D26):** Represents deep knowledge, academic growth, and official trust. This is your primary background color for headers and footers.
*   **Vibrant Amber (HEX: #F59E0B):** Represents energy, youth, and action. Used strictly for primary buttons, call-to-actions, and highlights.

### Secondary / Neutral Colors
*   **Sage Light (HEX: #F5F7F2):** A soft, off-white background color that is much easier on the eyes than pure white, giving the app a premium feel.
*   **Charcoal Text (HEX: #1F2937):** For primary body text. Never use pure black (#000000) for text as it causes eye strain.
*   **Muted Forest (HEX: #4B6354):** For secondary text, borders, and inactive UI elements.

---

## 3. Typography
The typography needs to be highly readable on mobile screens while maintaining a modern, tech-forward aesthetic.

*   **Primary Font (Headings):** **Plus Jakarta Sans**
    *   *Why?* It’s a geometric sans-serif that looks incredibly modern, clean, and friendly. It gives an immediate "tech startup" feel.
    *   *Usage:* All H1, H2, H3 elements and logo wordmarks. Use font-weight: 700 (Bold).
*   **Secondary Font (Body Text):** **Inter** or **Plus Jakarta Sans** (Regular)
    *   *Why?* Highly legible at small sizes. Perfect for event descriptions, dates, and locations.
    *   *Usage:* Paragraphs, UI elements, button text. Use font-weight: 400 (Regular) and 500 (Medium).

---

## 4. Logo & Visual Identity
The official logo encapsulates the core mission of the platform: connecting the ecosystem.

*   **The Logomark (The Network Node):**
    *   A stylized letter 'K' where the arms of the letter are made of connection nodes (dots connected by intersecting lines). This directly symbolizes a digital hub and cross-campus networking.
    *   ![KamConnect Official Logo](/Users/pelin/.gemini/antigravity/brain/6a909e00-5b20-4fb2-b38b-c5f13ef3f40f/kamconnect_logo_network_1782211164023.png)
*   **The Logotype:**
    *   The word "KamConnect" written in *Plus Jakarta Sans Bold*, with "Kam" in Forest Green and "Connect" in Vibrant Amber.

---

## 5. Brand Voice & Tone
How KamConnect speaks to its users:
*   **Encouraging & Direct:** "Discover your next big opportunity." (Not: "Please click here to view available academic seminars.")
*   **Community-Focused:** Use words like *we, us, our ecosystem, community*. 
*   **Clear & Professional:** Since you are dealing with university admins and lecturers, avoid excessive slang. Be precise but friendly.

---

## 6. UI/UX Styling Principles (For the Revamp)
When you rebuild this in Django + React:
1.  **Glassmorphism Accents:** Use subtle frosted-glass effects on top of the Forest Green headers to give it a premium 2026 feel.
2.  **Soft Shadows:** Ditch hard borders on event cards. Use soft, diffused drop shadows to make cards "float" off the Sage Light background.
3.  **Micro-animations:** Buttons should gently scale up on hover. Event cards should lift slightly when moused over to encourage clicking.
4.  **Generous Whitespace:** Don't cram events together. Let the UI breathe. Academic content can be text-heavy, so whitespace is your best friend for readability.
