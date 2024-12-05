## **Cat Chat Application**

A conversational application where users can interact with a chatbot to request images and details about different cat breeds. The application dynamically displays images and breed descriptions based on user input and provides an interactive experience with zoom functionality for images.

---

### **Key Functionalities**

1. **Chat Interaction**:
   - Users can request cat images by specifying a breed and number, e.g., `"Show me 5 images of Persian cats."`
   - If no breed or number is mentioned, the bot defaults to displaying **3 random cat images**.

2. **Dynamic Responses**:
   - The chatbot responds with:
     - A brief description of the breed.
     - Images of the specified or random cat breeds.
   - Information includes the breed's origin, temperament, and a detailed description.

3. **Image Zoom and Details**:
   - Clicking on an image opens a modal that:
     - Zooms into the image.
     - Displays additional breed information such as:
       - Name
       - Description
       - Origin
       - Temperament

4. **Error Handling**:
   - If an invalid breed or request is made, the bot responds gracefully by showing random cat images and a message explaining the fallback.

5. **Dark Mode Design**:
   - A clean, user-friendly UI styled in dark mode for a modern look.

---

### **How It Works**

1. **User Queries**:
   - Users can type queries in natural language, such as:
     - `"Show me 3 images of Bengal cats."`
     - `"Give me some random cats."`

2. **Bot Responses**:
   - The bot processes the query and responds with:
     - The number of images requested.
     - Detailed information about the breed (if available).
   - Example response:
     - `"Here are 3 images of Bengal cats."`
     - Images of Bengal cats appear, and clicking on them shows their details.

3. **Default Behavior**:
   - If no breed or number is mentioned:
     - The bot defaults to 3 random cat images.
     - Example response:
       `"Here are 3 images of random cats."`

4. **Interactive Image Modal**:
   - Clicking an image opens a modal displaying:
     - The image in a larger size.
     - The breed description below the image.
   - Users can close the modal by clicking outside it or pressing a close button.

---

### **Technologies Used**

1. **Backend**: 
   - **Flask** handles API requests and integrates with [The Cat API](https://thecatapi.com/) to fetch:
     - Cat images.
     - Breed descriptions.
   
2. **Frontend**:
   - **React** dynamically renders chat messages, images, and modal components for breed details.

3. **API**:
   - [The Cat API](https://thecatapi.com/):
     - Provides images and detailed information about cat breeds.

---

### **Usage Scenarios**

1. **Request Specific Breeds**:
   - Query: `"Show me 2 images of Siamese cats."`
   - Response: The bot displays 2 images of Siamese cats along with their breed details.

2. **Request Random Cats**:
   - Query: `"Show me some cats."`
   - Response: The bot displays 3 random cat images and a generic message.

3. **Zoom and Learn**:
   - Click on an image to open a modal for a larger view and additional details about the breed.

4. **Graceful Fallbacks**:
   - Query: `"Show me 5 images of an invalid breed."`
   - Response: The bot defaults to showing 3 random cat images with a message explaining the fallback.

---

### **Example Queries**

#### **1. Valid Query**
- Query: `"Show me 4 images of Bengal cats."`
- Response:
  ```
  Bot: Here are 4 images of Bengal cats.
  ```
- Images:
  - Each image is clickable for a zoomed view and additional details:
    - **Description**: "Bengals are fun and energetic cats."
    - **Origin**: "United States"
    - **Temperament**: "Alert, Agile, Energetic, Demanding, Intelligent"

#### **2. No Breed Specified**
- Query: `"Show me some cats."`
- Response:
  ```
  Bot: Here are 3 images of random cats.
  ```

#### **3. Invalid Query**
- Query: `"Show me 3 images of invalid_breed."`
- Response:
  ```
  Bot: The breed you requested is not available. Here are 3 images of random cats.
  ```

---

### **Future Enhancements**

1. **Streaming Responses**:
   - Incrementally display text and images for real-time feedback.
2. **Voice Integration**:
   - Allow users to request cat images using voice commands.
3. **Breed Selection**:
   - Add a dropdown menu to select breeds interactively.
