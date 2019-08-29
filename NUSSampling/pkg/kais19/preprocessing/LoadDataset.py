#-*- coding:Utf-8 -*-

# NUSSampling
# Copyright (c) 2019  Lamine Diop (1;2), Cheikh Talibouya Diop (1), Arnaud Giacometti (2), Dominique Li (2) and Arnaud Soulet (2)
# (1) University of Gaston Berger of Saint-Louis, Senegal, Email: {diop.lamine3, cheikh-talibouya.diop}@ugb.edu.sn
# (2) University of Tours, France, Email: {arnaud.giacometti, dominique.li, arnaud.soulet}@univ-tours.fr

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# ---------------------------------------------------------------------

__author__ = "DIOP Lamine BSF"

class LoadDataset(object):
    
    def __init__(self, baseSequence,indiceClass):
        self.delimiteurSequence = str('-2 ')
        self.dataset = list()
        self.size = 0
        with open(baseSequence, 'r') as base:
            line=base.readline()
            while line:
                self.dataset.append(line.replace("-2","").replace("\n",""))
                line=base.readline()
        self.dataset = self.dataset
        self.size=self.dataset.__len__()
    
    def dataset(self):
        return self.dataset
