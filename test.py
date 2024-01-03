# import time
# import threading

# def api1():
#     print("call 1st API")
#     time.sleep(4)
#     print("1st API finish")
  
# def api2():
#     print("call 2st API")
#     time.sleep(3)
#     print("2nd API finish")

# start = time.time()

# # create threads
# t1 = threading.Thread(target=api1, name='t1')
# t2 = threading.Thread(target=api2, name='t2')  

# # start threads
# t1.start()
# t2.start()

# # wait untill all threads finished
# t1.join()
# t2.join()

# print(time.time()-start)

# """
# call 1st API
# call 2st API
# 2nd API finish
# 1st API finish
# 4.003810882568359
# """

# import threading
# import mouse
# import keyboard

# mouse_events = []


# mouse.hook(mouse_events.append)
# keyboard.start_recording()

# keyboard.wait("a")

# mouse.unhook(mouse_events.append)
# keyboard_events = keyboard.stop_recording()

# #Keyboard threadings:

# k_thread = threading.Thread(target = lambda :keyboard.play(keyboard_events))
# k_thread.start()

# #Mouse threadings:

# m_thread = threading.Thread(target = lambda :mouse.play(mouse_events))
# m_thread.start()

# #waiting for both threadings to be completed

# k_thread.join() 
# m_thread.join()



# /home/kaloyan/web_scraper/Projects/test_scraper.py