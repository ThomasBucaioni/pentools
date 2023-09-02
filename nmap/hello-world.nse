local shortport = require "shortport"

description = [[
Hello World script
]]

categories = {"safe"}

portrule = shortport.http

action = function(host,port)
  local output = "Hello World"
  return output
end

