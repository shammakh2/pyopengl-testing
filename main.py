import glfw
from OpenGL.GL import *
from pyrr import *
import pyrr
import numpy as np
from PIL import Image

vertex_src = """
# version 330
layout(location = 0) in vec3 a_position;
layout(location = 1) in vec2 texC;

uniform mat4 proj;


out vec2 texCord;

void main()
{
    gl_Position = proj * vec4(a_position, 1.0);
    texCord = texC;
}
"""

fragment_src = """
# version 330

in vec2 texCord;
out vec4 color;

uniform sampler2D u_texture;

void main()
{
    vec4 texColor = texture(u_texture, texCord);
    color = texColor;
}
"""

# initializing glfw library
if not glfw.init():
    raise Exception("glfw can not be initialized!")

glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

# creating the window
window = glfw.create_window(6*200, 3*200, "My OpenGL window", None, None)

# check if window was created
if not window:
    glfw.terminate()
    raise Exception("glfw window can not be created!")


# set window's position
glfw.set_window_pos(window, 100, 100)

# make the context current
glfw.make_context_current(window)
glfw.swap_interval(1)


print(glGetString(GL_VERSION))
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

prog = glCreateProgram(1)

vs = glCreateShader(GL_VERTEX_SHADER)
fs = glCreateShader(GL_FRAGMENT_SHADER)

glShaderSource(vs,vertex_src)
glShaderSource(fs, fragment_src)

glCompileShader(vs)
glCompileShader(fs)

glAttachShader(prog, vs)
glAttachShader(prog, fs)

glLinkProgram(prog)

glUseProgram(prog)


vertices = [
            -0.5, -0.5, 0, 0, 1,
            0.5, -0.5, 0, 1, 1,
            -0.5, 0.5, 0, 0, 0,
            0.5, 0.5, 0, 1, 0
            ]

indices = [
            0,1,2,
            2,1,3
]


verti = (ctypes.c_float * len(vertices))(*vertices)
indi = (ctypes.c_uint * len(indices))(*indices)

vao = glGenVertexArrays(1)
glBindVertexArray(vao)

vbo = glGenBuffers(1)
ibo = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, vbo)
glBufferData(GL_ARRAY_BUFFER, sizeof(verti),verti, GL_STATIC_DRAW )
glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 5*sizeof(ctypes.c_float), ctypes.c_void_p(0))
glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 5*sizeof(ctypes.c_float), ctypes.c_void_p(3*sizeof(ctypes.c_float)))

glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ibo)
glBufferData(GL_ELEMENT_ARRAY_BUFFER, sizeof(indi), indi, GL_STATIC_DRAW )

# ixd = glGetAttribLocation(prog, "color")
# glEnableVertexAttribArray(ixd)
# glVertexAttribPointer(ixd, 3, GL_FLOAT, GL_FALSE, 6*sizeof(ctypes.c_float), ctypes.c_void_p(3*sizeof(ctypes.c_float)))


picData = Image.open("bf.png")
pcDat = picData.convert("RGBA").tobytes()

tex = glGenTextures(1)
glBindTexture(GL_TEXTURE_2D, tex)


glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_BORDER)
glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_BORDER)

glActiveTexture(GL_TEXTURE0)


glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA8, picData.size[0], picData.size[1], 0, GL_RGBA, GL_UNSIGNED_BYTE, pcDat)


uTex = glGetUniformLocation(prog, "u_texture")
glUniform1i(uTex, 0)

glClearColor(0.0, 0.05, 0.05, 1)

pu = glGetUniformLocation(prog, "proj")
proj = Matrix44.orthogonal_projection(-2.0, 2.0, -1, 1, -1.0, 1.0)
view = pyrr.matrix44.create_from_translation( Vector3([0.5, 0.5, 0.0]))
glUniformMatrix4fv(pu, 1, GL_FALSE, proj * view)


while not glfw.window_should_close(window):
    glfw.poll_events()
    glClear(GL_COLOR_BUFFER_BIT)
    glDrawElements(GL_TRIANGLES, 8, GL_UNSIGNED_INT, None)
    glfw.swap_buffers(window)
# terminate glfw, free up allocated resources
glfw.terminate()