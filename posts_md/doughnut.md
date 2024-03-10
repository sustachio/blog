Turn Your Text Into Doughnuts
Project
2023-5-10
Have you ever wanted to turn any text into a doughnut? No? Well I did, and I made a tool to do just that!

Introducing [Doughnut Text Formater](https://github.com/sustachio/doughnut-text-formater), a tool to make your text doughnut shaped. It uses lots of math to make the perfect doughnuts out of any text.

It works with short bits of text:
    
      Convert a  
     ny b   lock 
      of     tex 
     t into a d  
      oughnut!   

And larger chunks of text:
    
                  Phasellus nec est e               
               u metus dapibus sagittis.            
            Phasellus at cursus arcu. Quisq         
          ue laoreet nisi sit amet accumsan f       
         acilisis. In facilisis risus eget feli     
       s scelerisque, id interdum nibh lobortis.    
       Aenean gravida, nulla gravida viverra inte   
      rdum, ligula orci           commodo risus, f  
     eugiat interdum               leo massa eu mas 
     sa. Mauris fini                bus fringilla l 
     obortis. Nunc                   condimentum ac 
     cumsan condime                  ntum. Sed quis 
      bibendum ex.                  Aliquam erat vo 
     lutpat. Aliquam                pellentesque, o 
     dio id ullamcorpe            r placerat, maur  
      is sapien lobortis d    ui, a bibendum mauri  
       s sem quis ipsum. Nam vitae eleifend liber   
        o. Cras at semper sapien, id lobortis j     
          usto. Vestibulum ante ipsum primis i      
            n faucibus orci luctus et ultric        
              es posuere cubilia curae; Pr          
                 oin fringilla gravida              
                      ultrices.                     
                                                    

Just like my [random-css]({{ url_for('post', post_id='never-write-a-line-of-css-again') }}) tool, I built this one right into this website! Simply add `?doughnut` to the end of any url on this site.

Here are some links to try it out with:

- <a href="{{ url_for('home') }}?doughnut" target="_self">Home</a>
- <a href="{{ url_for('find_me') }}?doughnut" target="_self">Find Me</a>
- <a href="{{ url_for('post', post_id='turn-your-text-into-doughnuts') }}?doughnut" target="_self">This Post</a>

If you want to try it out yourself, it is documented on its [github]([https://github.com/sustachio/](https://github.com/sustachio/doughnut-text-formater)).
