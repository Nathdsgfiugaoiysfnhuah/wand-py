require("gun_enums")
require("gun_actions")
require("io")

file = io.open("translations.csv","r")
translations = {}
io.input(file)
io.read()
while true do
  line = io.read()
  if not line then break end
  parsed = ""
  target = ""
  count = 0
  ptr = 1
  while true do
    char = line:sub(ptr,ptr)
    ptr = ptr + 1
    if char ~= "," then
      if count == 1 then target = target .. char
      else parsed = parsed .. char end
    else
      count = count + 1
      if count == 2 then break end
    end
  end
  translations[parsed] = target
end
io.close(file)

content = [[
def get_info():
  return {]]
for k,v in pairs(translations) do
  content = content.."\""..k.."\":\""..v:gsub("\"","'").."\","
end
content = content.."}"

file = io.open("d_map.py","w")
io.output(file)
io.write(content)
io.close(file)


content = [[
def get_info():
  return []]
for k,v in ipairs(actions) do
  content = content .. "(\"" .. v.name .. "\"," .. v.type .. ",\"" .. v.sprite .. "\",\"" .. v.id .. "\"),"
end
content = content.."]"

file = io.open("d_types.py","w")
io.output(file)
io.write(content)
io.close(file)

