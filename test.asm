LOAD B #1 ; test comment
LOAD C #10
CALL loop

end:
JUMP end

loop:
ADD A B
EQUAL A #10
JUMP loop
RETURN
