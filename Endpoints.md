| **Resource**   | **Method** | **Endpoint** | **Description** |
|---------------|-----------|-------------|----------------|
| **Tutorials** | GET       | `/tutorials/` | List all tutorials |
|               | POST      | `/tutorials/` | Create a new tutorial |
|               | GET       | `/tutorials/{title}/` | Retrieve a specific tutorial by title |
|               | PUT       | `/tutorials/{title}/` | Update a tutorial |
|               | PATCH     | `/tutorials/{title}/` | Partially update a tutorial |
|               | DELETE    | `/tutorials/{title}/` | Delete a tutorial |
|               | GET       | `/tutorials/{title}/categories/` | Get categories associated with a specific tutorial |
|               | GET       | `/tutorials/search_by_title/?title=<value>` | Search tutorials by title |
| **Categories** | GET       | `/categories/` | List all categories |
|               | POST      | `/categories/` | Create a new category |
|               | GET       | `/categories/{slug}/` | Retrieve a specific category by slug |
|               | PUT       | `/categories/{slug}/` | Update a category |
|               | PATCH     | `/categories/{slug}/` | Partially update a category |
|               | DELETE    | `/categories/{slug}/` | Delete a category |
|               | GET       | `/categories/{slug}/courses/` | Get courses in a specific category |
|               | GET       | `/categories/search_by_name/?name=<value>` | Search categories by name |
| **Courses**   | GET       | `/courses/` | List all courses |
|               | POST      | `/courses/` | Create a new course |
|               | GET       | `/courses/{pk}/` | Retrieve a specific course by ID |
|               | PUT       | `/courses/{pk}/` | Update a course |
|               | PATCH     | `/courses/{pk}/` | Partially update a course |
|               | DELETE    | `/courses/{pk}/` | Delete a course |
|               | GET       | `/courses/{pk}/sections/` | Get sections within a specific course |
|               | GET       | `/courses/{pk}/lessons/` | Get lessons related to a course |
|               | GET       | `/courses/search_by_title/?title=<value>` | Search courses by title |
| **Sections**  | GET       | `/sections/` | List all sections |
|               | POST      | `/sections/` | Create a new section |
|               | GET       | `/sections/{slug}/` | Retrieve a specific section by slug |
|               | PUT       | `/sections/{slug}/` | Update a section |
|               | PATCH     | `/sections/{slug}/` | Partially update a section |
|               | DELETE    | `/sections/{slug}/` | Delete a section |
|               | GET       | `/sections/{slug}/lessons/` | Get lessons in a specific section |
|               | GET       | `/sections/search_by_title/?title=<value>` | Search sections by title |
| **Lessons**   | GET       | `/lessons/` | List all lessons |
|               | POST      | `/lessons/` | Create a new lesson |
|               | GET       | `/lessons/{pk}/` | Retrieve a specific lesson by ID |
|               | PUT       | `/lessons/{pk}/` | Update a lesson |
|               | PATCH     | `/lessons/{pk}/` | Partially update a lesson |
|               | DELETE    | `/lessons/{pk}/` | Delete a lesson |
|               | GET       | `/lessons/by_parent/?content_type=<value>&object_id=<value>` | Get lessons by parent type (Course/Section) and ID |
|               | GET       | `/lessons/search_by_title/?title=<value>` | Search lessons by title |
