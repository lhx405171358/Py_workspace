@echo off
set sharepath=%*
set disk=%sharepath:~0,2%
%disk%
cd %sharepath%
@py.exe -2 -m SimpleHTTPServer 7777
@pause