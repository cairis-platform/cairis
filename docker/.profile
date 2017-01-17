mysql -h localhost -u root <<!
set global max_sp_recursion_depth = 255;
flush tables;
flush privileges;
!
