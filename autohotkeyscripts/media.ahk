Gosub, %1%
return

next:
Send {Media_Next}
return

previous:
Send {Media_Prev}
return

pause:
Send {Media_Play_Pause}
return

play:
Send {Media_Play_Pause}
return

stop:
Send {Media_Stop}
return

volup:
Send {Volume_Up 5}
return

voldown:
Send {Volume_Down 5}
return

mute:
Send {Volume_Mute}
return