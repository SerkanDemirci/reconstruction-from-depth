class Vertex():
    def __init__(self, position = [0, 0, 0], color = [0, 0, 0], texture_coordinates= [0 ,0]):
        self.position = position[:]
        self.color    = color[:]
        self.index    = -1
        self.texture_coordinates = texture_coordinates

    def _set_position(self,d, value):
        self.position[d] = value

    def _set_color(self,d, value):
        self.color[d] = value

    x = property(lambda self: self.position[0], lambda self, value: self._set_position(0, value));
    y = property(lambda self: self.position[1], lambda self, value: self._set_position(1, value));
    z = property(lambda self: self.position[2], lambda self, value: self._set_position(2, value));

    r = property(lambda self: self.color[0], lambda self, value: self._set_color(0, value));
    g = property(lambda self: self.color[1], lambda self, value: self._set_color(1, value));
    b = property(lambda self: self.color[2], lambda self, value: self._set_color(2, value));

class Face():
    def __init__(self, vertices, texture_coordinates = None):
        self.vertices = vertices
        self.index  = -1


class PLY(object):
    def __init__(self):
        self.vertices = []
        self.faces  = []

    def add_vertex(self, vertex):
        # Check First time adding vertex
        if (vertex.index == -1):
            # Add vertex and set values
            vertex.index = len(self.vertices)
            self.vertices.append(vertex)
        else:
            #Else update the vertex
            self.vertices[vertex.index] = vertex

        return vertex.index

    def add_face(self, face):
        # Check First time adding vertex
        if (face.index == -1):
            # Add vertex and set values
            face.index = len(self.faces)
            self.faces.append(face)
        else:
            #Else update the vertex
            self.faces[face.index] = face

        return face.index

    def save(self, path, **kwargs):
        color = kwargs.pop('color', 'vertex')

        vertex_color = color == 'vertex'
        texture_mapped = color == 'texture'

        if (vertex_color == False and texture_mapped == False):
            raise Exception("Incorrect color type".format(name))

        with open(path, 'w') as fp:
            fp.write("ply\n");
            fp.write("format ascii 1.0\n");

            # Vertex Definition
            fp.write("element vertex {}\n".format(len(self.vertices)))

            fp.write("property float x\n")
            fp.write("property float y\n")
            fp.write("property float z\n")

            if (vertex_color):
                fp.write("property uchar red\n")
                fp.write("property uchar green\n")
                fp.write("property uchar blue\n")

            if (texture_mapped):
                fp.write("property float s\n")
                fp.write("property float t\n")

            # Face Definition
            if (len(self.faces) > 0):
                fp.write("element face {}\n".format(len(self.faces)))
                fp.write("property list uchar int vertex_index\n")

            fp.write("end_header\n")

            for vertex in self.vertices:
                fp.write("{} {} {} ".format(vertex.x, vertex.y, vertex.z));

                if (vertex_color):
                    r = max(0, min(1, vertex.r))
                    g = max(0, min(1, vertex.g))
                    b = max(0, min(1, vertex.b))

                    r = int(255 * r)
                    g = int(255 * g)
                    b = int(255 * b)

                    fp.write("{} {} {}".format(r, g, b));

                if (texture_mapped):
                    fp.write("{} {}".format(vertex.texture_coordinates[0], 1 - vertex.texture_coordinates[1]))


                fp.write("\n");

            if (len(self.faces) > 0):
                for face in self.faces:
                    fp.write("{} ".format(len(face.vertices)))
                    for vertex in face.vertices:
                        fp.write("{} ".format(vertex.index))

                    fp.write("\n")
