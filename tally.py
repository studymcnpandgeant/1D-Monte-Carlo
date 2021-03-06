import numpy as np
import transport as tr

class k_code_tally:
    def num_par(self, kcode):
        self.num_par = int(kcode[0])

    def num_gen(self, kcode):
        self.num_gen = int(kcode[1])

    def num_skip_gen(self, kcode):
        self.num_skip_gen = int(kcode[2])

    def init_k(self, kcode):
        self.init_k = kcode[3]

    def k_tally(self, k):
        self.k_tally = np.zeros(k.num_gen - k.num_skip_gen)
        self.k_tally[0] = 1.0

    def accumulate_k(self, iter, k):
        self.k_tally[iter] = k


def init_k_tally(kcode):
    k = k_code_tally()
    k.num_par(kcode)
    k.num_gen(kcode)
    k.num_skip_gen(kcode)
    k.init_k(kcode)
    k.k_tally(k)
    return k


# Right now it just takes in a dummy cell
class mesh_tally():
    def init_mesh(self, mesh):
        self.mesh = np.zeros((mesh, 2))

    def init_flux(self, mesh):
        self.flux = np.zeros((mesh, 2))

    def init_fission_source(self, mesh):
        self.fission_source = np.zeros(mesh)

    def accumulate(self, mesh, p, tr_len):
        for i, x in enumerate(mesh):
            if i == p.cell:
                if p.enrg == 1:
                    mesh[i][0] += tr_len
                else:
                    mesh[i][1] += tr_len
                break

    def gen_flux(self, num_part, geo):
        for x in geo.cells:
            for i, y in enumerate(self.mesh[x]):
                self.flux[x, i] = y / (num_part * (geo.pos[x+1] - geo.pos[x]))

    def gen_fission_source(self, geo, mat_array):
        xc = tr.get_XC(1, 0, mat_array)
        for i, y in enumerate(geo.mat):
            x = int(y)
            xc.get_nu(1, x, mat_array)
            nu_f = xc.nu
            xc.get_nu(2, x, mat_array)
            nu_t = xc.nu
            xc.get_fiss_xc(1, x, mat_array)
            fiss_f = xc.fiss_xc
            xc.get_fiss_xc(2, x , mat_array)
            fiss_t = xc.fiss_xc
            self.fission_source[i] = nu_f * fiss_f * self.flux[i, 0] + nu_t * fiss_t * self.flux[i, 1]


def init_mesh_tally(geo):
    mt = mesh_tally()
    mt.init_mesh(len(geo.cells))
    mt.init_flux(len(geo.cells))
    mt.init_fission_source(len(geo.cells))
    return mt

