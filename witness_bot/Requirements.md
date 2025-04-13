# Witness Interrogation Chatbot Requirements

## General Description
The chatbot will simulate a witness interrogation process, inspired by the ELIZA program. It will adopt a non-directive questioning style to encourage the witness to provide detailed and relevant information.

## Functional Requirements
1. **Input Handling**:
   - Accept natural language input from the user (witness).
   - Handle incomplete or ambiguous statements gracefully.

2. **Response Generation**:
   - Use pattern matching to generate responses based on the user's input.
   - Reflect the user's statements to encourage elaboration (e.g., "Can you tell me more about that?").
   - Ask open-ended questions to gather more details.

3. **Context Awareness**:
   - Maintain a conversational context to refer back to previous statements.
   - Avoid repetitive or irrelevant responses.

4. **Customization**:
   - Allow configuration of the chatbot's tone (e.g., formal or informal).
   - Support domain-specific vocabulary for legal or investigative contexts.

5. **Error Handling**:
   - Provide meaningful responses when the input is unclear or off-topic.
   - Avoid breaking the conversation flow due to unexpected input.

## Additional Interview Information Requirements
- Indirectly inquire about basic personal details (e.g., name, age, occupation) without making the witness feel interrogated.
- Prompt for contextual information such as:
  - Time and location of events.
  - Description of involved persons or objects.
  - Sequence of events and any discrepancies.
- Encourage the witness to elaborate by reflecting statements and gently probing for additional details.

## Conversation Continuity
- Design the conversation to remain open-ended, allowing the witness to continue elaborating as long as they wish.
- Continuously offer reflective prompts (e.g., "Erzählen Sie mir mehr darüber", "Wie ging es danach?") to sustain the dialogue.
- Ensure that every answer includes an opportunity for follow-up, reinforcing the non-directive style.
