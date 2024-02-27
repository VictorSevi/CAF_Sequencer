
############################################################# Test actions definition ############################################################################
import tkinter as tk


class text_action:
   def __init__(self,gui_item,next_action=None,cmd=False, row=0 ):
      self.gui_item = gui_item
      self.next_action = next_action
      self.there_is_next = False
      self.row=row
      self.termminal=False
      
   def execute(self,i):
      self.frame_loc=tk.Frame(self.gui_item,bg='white', borderwidth = 2, relief="solid")
      self.frame_loc.pack(fill=tk.BOTH, expand=True)
      #self.frame_loc.grid(row=self.row,column=0,sticky='nswe')
      
   def next_act(self):
      self.destroy()
      if self.there_is_next:self.next_action.enable()
      else: self.terminal_func()

   def set_next_acion(self,next_action):
      self.next_action=next_action
      self.there_is_next= True

   def destroy(self): self.frame_loc.destroy()

   def set_end_func(self,func): self.terminal_func=func

   def is_CA(self): return False



class MFA_test_action(text_action):
   def __init__(self,gui_item,text, row=0):
      super().__init__(gui_item,row=row)
      self.text = text

   def execute(self,i):
      super().execute(i)

      #app diseño app
      self.frame_loc.columnconfigure(0, weight=10)
      self.frame_loc.columnconfigure(1, weight=1)
      self.frame_loc.columnconfigure(1, weight=1)
      self.frame_loc.rowconfigure(0, weight=4 )
      self.frame_loc.rowconfigure(1, weight=1 )


      #se crea la etiqueta de texto
      order_text = tk.Label(self.frame_loc, text=self.text,pady=50, font=("Arial",15), bg='white')
      order_text.grid(column=0,row=0)
        
      #se crea el boton de done
      self.boton_OK = tk.Button(self.frame_loc, text="Done",height=5,font=("Arial",12),command=self.next_act)
      self.boton_OK.grid(column=0,row=1,sticky="nswe", pady=20, padx=40)

      self.boton_OK.config(state="disable")

   def enable(self):
      self.boton_OK.config(state="normal")

class MCA_test_action(text_action):
   def __init__(self,gui_item,text, result='NE',row=0):
      super().__init__(gui_item,row=row)
      self.text = text
      self.result = result

   def execute(self,i):
      super().execute(i)

      #app diseño app
      self.frame_loc.columnconfigure(0, weight=10)
      self.frame_loc.columnconfigure(1, weight=1)
      self.frame_loc.rowconfigure(0, weight=5)
      self.frame_loc.rowconfigure(1, weight=2)

      #se crea la etiqueta de texto
      order_text = tk.Label(self.frame_loc, text=self.text,pady=50, font=("Arial",15), bg='white',anchor='center')
      order_text.grid(column=0,row=0,sticky="nswe")

      #se crea la etiqueta de texto
      bg_code = '#C4FFC4' if self.result =='OK' else ('#FFCCCC' if self.result =='NOK' else'#ECECEC')
      result_text = tk.Label(self.frame_loc, text=self.result,padx=50, font=("Arial",20), bg=bg_code, anchor='center')
      result_text.grid(column=1,row=0,sticky="nswe", pady=10, padx=10)
        
      #marco botones
      self.buttons_frame=tk.Frame(self.frame_loc, bg='white')
      self.buttons_frame.grid(row=1,column=0,sticky="nswe")
      self.buttons_frame.columnconfigure(0, weight=1)
      self.buttons_frame.columnconfigure(1, weight=1)

      #se crea el boton de done
      boton_OK = tk.Button(self.buttons_frame, text="OK", font=("Arial",12),command=self.set_ok,bg='green', heigh=5)
      boton_OK.grid(column=0, row=0,sticky="nswe", pady=20, padx=40)
      #boton_OK.pack()

      #se crea el boton de done
      boton_NOK = tk.Button(self.buttons_frame, text="NOK", font=("Arial",12),command=self.set_nok, bg="red",heigh=5)
      boton_NOK.grid(column=1,row=0,sticky="nswe", pady=20, padx=40 )
      #boton_NOK.pack()
      
      for widget in self.buttons_frame.winfo_children():
         widget.config(state="disabled")

   
   def enable(self):
      for widget in self.buttons_frame.winfo_children():
         widget.config(state="normal")

   def set_ok(self): 
      self.result='OK'
      self.next_act()
      
   def set_nok(self): 
      self.result='NOK'
      self.next_act()

   def is_CA(self): return True

   def get_result(self): return self.result
