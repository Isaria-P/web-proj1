# Journal
What did I complete? 
What am I working on next? 
What is blocking me?

#   Week 1
day 1: 
What did I complete?  came up with the Website Idea
What am I working on next? Figma design
What is blocking me? figuring out how to plan the code 


day 2:
What did I complete?  Project Summary, repository, user story, target User. 
What am I working on next?  Figma Design
What is blocking me? mobile layouts

day 3
What did I complete? Problem Being Solved, Project Scope, Features, Must Have Features, Frontend Track, Design Rationale, Proposed Database Models
What am I working on next?Route/endpoint List, Api, Project structure, Proposed Relationships.
What is blocking me? focusing

day 4:
What did I complete? Route/endpoint List, Api, Project structure, Proposed Relationships
What am I working on next?  Figma Design
What is blocking me?  i need to see other examples or a templates

day 5:
What did I complete? researching modeules

What am I working on next?  Figma Design
What is blocking me?  i need to see other examples or a templates

day 6:
What did I complete?setting up project

What am I working on next?  Figma Design
What is blocking me?  i need to see other examples or a templates

day 7 tues 
What did I complete? worked on database
What am I working on next? fixing errors
What is blocking me? having errors


day 8 wed 
What did I complete? fixing modules errors
What am I working on next? working on fom validation
What is blocking me? time

day 9 thurs 
What did I complete? validation
What am I working on next? errors
What is blocking me? 

day 10 Monday 
What did I complete? prototyping research, planning
What am I working on next? errors validation
What is blocking me? i not sure what im doing wrong

day 11 tues 
What am I working on next? errors validation
What is blocking me? i not sure what im doing wrong, getting annoyed getting confused

day 12 wedn 
What did I complete? fixed database error
What am I working on next? working on fixing the program in time for the presentation 
What is blocking me? having enough time

day 13 thurs 
What did I complete? researching database image storing
What am I working on next? implementing what i learned in my code 
What is blocking me? having enough time

day 14 friday 
What did I complete?looking up issues 
What am I working on next? implementing what i learned in my code 
What is blocking me? having enough time

day 15 sunday 
What did I complete? researching database image storing
What am I working on next? implementing what i learned in my code 
What is blocking me? having enough time

day 16 monday 
What did I complete? researching database image storing
What am I working on next? implementing what i learned in my code 
What is blocking me? having enough time

day 17 tuesday 
What did I complete? researching database image storing
What am I working on next? implementing what i learned in my code 
What is blocking me? having enough time

day 18 wednesday 
What did I complete? adding comment section and profile
What am I working on next?errors
What is blocking me? time and will power


day 19 thursday 
What did I complete? presenting my previous file because i was not able to fix the errors on time
What am I working on next? implementing a Delet & Edit section.
What is blocking me? 

day 20 Friday 
What did I complete? added the my account section where users can view the post they posted, and update and delete the post.
What am I working on next? fix edit btn error. comment section || update & delete
What is blocking me?  blocking out time to focus.

day 21 Friday 
What did I complete? fixed major errors and styling to the MyAccount section .
What am I working on next? comment section 
What is blocking me?  family dram is distracting

day 22 saturday 
What did I complete? comment.jinja  comment Models, route - researched adding action buttons/ styling my My Account-profile page
What am I working on next? category.jinja category Models & route 
What is blocking me? 
day 23 Sunday 
What did I complete? researched adding action buttons/ styling my My Account-profile pae
What am I working on next? comment section 
What is blocking me?  family dram is distracting

day 24 Monday 
What did I complete? testing view.jinja adding + profile.jinja - Lookuping up category models + route what do they look like. category moddels
What am I working on next? dynamicly load the page category section / nav category
What is blocking me? 

day 25 tuesday category day/ buttons + testing 
What did I complete? testing view.jinja adding + profile.jinja - Lookuping up category models + route what do they look like. category models
What am I working on next? category acction buttons

day 26 thursday
What did I complete? fix cam edit error, added comment edit and delete
What am I working on next? write out the models/routes and forms for future users. finalizing the the visual





# presentation
https://docs.google.com/presentation/d/1SMZFTYyJuKsNJ37aSa3UvMXxPtapxYtl2Gf5AfCqaOw/edit?usp=sharing


# figma 

[127.0.0.1 - - \[13/Aug/2026 09:51:29\] "GET /static/css/main.css HTTP/1.1" 304 -](https://www.figma.com/proto/CA9CsbZueQRGMre8iXCrpQ/CMI-Mood-Board?node-id=2014-2137&p=f&t=O0bQzoSfekQXj60v-1&scaling=contain&content-scaling=fixed&page-id=0%3A1)

--
Accounts.id
     │
     │
     ▼
Cams.author
     │
     │
     ▼
Comments.cam_id → Cams.id

Comments.author_id → Accounts.id

_____-___________-_________-_________-____________-________-___
DataClass

Cam: id, title, content, img, category, author_id, created, author_username

Comment: id, body, created, author_id, cam_id, author_username

models

CamModel(Model):
   insert(title, sontent, img, category, author_id)
   get(cam_id)
   get_with_author(cam_id)
   account_cams(account_id)
   latest()
   get_comments_with_authors(comment_id)
   update(cam_id, title, content, category, img)
   delete(cam_id)   
  get_by_category(category)

CommentModel(Model):
   insert(body, cam_id, author_id)
   for_cam(cam_id)
   account_comments(account_id)
   update(comment_id)
   delete(comment_id)


_____-___________-_________-_________-____________-________-___

routes

cams
GET("/") -  index() 
POST('/') - upload_file()
GET("/create") - create()
POST("/create") - create_submit()
GET, POST("/view/<int:cam_id>) - view(cam_id)
GET("/edit/<int:cam_id>") - edit(cam_id)
POST("/edit/<int:cam_id>") - edit_submit(cam_id)
POST("/delete/<int:cam_id>") - delete(cam_id)
GET("/category/<category>") - category(category)
GET("/comment/edit/<int:comment_id>")- comment_edit(comment_id)
POST("/comment/edit/<int:comment_id>") - comment_edit_submit(comment_id)

accounts
needs 2 finalize


_____-___________-_________-_________-____________-________-___


Form 

cams -
CamCreateForm(
   title, 
   content, 
   img, 
   category
)

 accounts -  
LoginForm(
  email,
  password
)
