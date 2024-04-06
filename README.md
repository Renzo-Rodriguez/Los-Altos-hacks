# Los-Altos-hacks

Project including Renzo Rodriguez Eric Cao, lam Nguyen and James Kim

To run this project, cd into the directory

first enter the  virtual environment:

  windows:
  
    ./backend/back/bin/activate
    
  linux:
  
    source backend/back/bin/activate

 then, with pip  run
 
   windows:
   
     pip install django, pymongo
   
   linux:
   
     pip3 install django,pymongo

  
Also make sure that you have mongodb, in this project we are using mongodb atlass


 to install mongo db on debian based distros follow this:
 
 https://medium.com/@arun0808rana/mongodb-installation-on-debian-12-8001d0dafb56

 otherwise I am not sure what to tell you

 To install mongodb Atlas  follow this:
 
 https://www.mongodb.com/blog/post/introducing-local-development-experience-atlas-search-vector-search-atlas-cli

 on linux run:
 
  sudo systemctl start mongod && sudo systemctl enable mongod
  
 to run the backend server cd into backend and run:

  py manage.py runserver (windows)

  python3 manage.py runserver (debian)


hope this helps 
:)























