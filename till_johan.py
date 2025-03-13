# Scrip that plots ship geometry related particulars e.g. all kinds of dimension and positions of devices and sensors that exists in the ship file
# Created ewi and axa - 2023-10-20

import json
import os
import warnings

from descartes import PolygonPatch
from matplotlib.collections import PatchCollection
import matplotlib.pyplot as plt
import numpy as np
from shapely.geometry import Polygon
from shapely.geometry.multipolygon import MultiPolygon

from shipdict_descriptions import get_ShipFile


def _plot_arrow(lpp, x_pos, y_pos, label, style, from_, to_, col, show_mid=True):
    """Plots a dubbel sided arrow"""
    plt.plot(x_pos, y_pos, style, label=label)
    # fmt: off
    if show_mid:
        if x_pos[0] == x_pos[1]:
            plt.plot([x_pos[0] - 0.3, x_pos[0] + 0.3],
                     [y_pos[0] + y_pos[1], y_pos[0] + y_pos[1]], style, lw=2)
        else:
            plt.plot([x_pos[0] + x_pos[1], x_pos[0] + x_pos[1]],
                     [y_pos[0] - 0.3, y_pos[0] + 0.3], style, lw=2)
    
    plt.arrow(x_pos[0], y_pos[0], -from_, -to_, shape="full", lw=0, 
              length_includes_head=True, head_width=0.01 * lpp, facecolor=col)
    plt.arrow(x_pos[1], y_pos[1], from_, to_, shape="full", lw=0,
              length_includes_head=True, head_width=0.01 * lpp, facecolor=col)
    # fmt: on


def _get_blade(propeller_xpos, propeller_ypos, propeller_diameter, hub_d) -> list:
    """Returns a list with radius of y-axis and the blade geometires"""
    u = propeller_diameter / 4 + hub_d / 4  # x-position of the center
    a = propeller_diameter / 2 - hub_d / 2  # radius on the x-axis
    b = propeller_diameter / 2 * 0.3  # radius on the y-axis

    t = np.linspace(0.0, 2 * np.pi, 20)
    blade_x = a * np.cos(t) / 2
    blade_y = b * np.sin(t) / 2

    blade_top_x = blade_y
    blade_top_y = blade_x + u
    blade_top_x = blade_top_x + propeller_xpos
    blade_top_y = blade_top_y + propeller_ypos

    blade_bottom_x = blade_y
    blade_bottom_y = blade_x - u
    blade_bottom_x = blade_bottom_x + propeller_xpos
    blade_bottom_y = blade_bottom_y + propeller_ypos
    return blade_top_x, blade_top_y, blade_bottom_x, blade_bottom_y, b


def _get_hub(propeller_xpos, propeller_ypos, hub_d, b) -> list:
    """Returns a list with the hub geometries"""
    hub_x = np.array([-b / 2, b / 2, b / 2, -b / 2, -b / 2])
    hub_y = np.array([-hub_d / 2, -hub_d / 2, hub_d / 2, hub_d / 2, -hub_d / 2])
    hub_x = hub_x + propeller_xpos
    hub_y = hub_y + propeller_ypos
    return hub_x, hub_y


class TopView:
    def __init__(self, shipdict, store_path=""):
        self.shipdict = shipdict
        self.ship_class = get_ShipFile(shipdict)
        self.save_path = store_path

    def plot_ship_plot_contour(self, axes):
        """Plot shipfile "PLOT_CONTOUR section"""
        if hasattr(self.ship_class, "plot_contour"):
            if len(self.ship_class.plot_contour) == 0:
                warnings.warn("Error no PLOT_CONTOUR was defined")
                return
            contourlist = self.ship_class.plot_contour[0]
            for j in range(len(contourlist)):
                temp = contourlist[j][0]
                contourlist[j][0] = contourlist[j][1]
                contourlist[j][1] = temp
        else:
            warnings.warn(
                "Error no PLOT_CONTOUR was defined trying to use contour_data"
            )
            contourlist = []
            for x, y in zip(
                self.ship_class.contour_data.xqc, self.ship_class.contour_data.yqc
            ):
                contourlist.append([x, y])
        polygons = [Polygon(x) for x in [contourlist]]
        multipolygon = MultiPolygon(polygons)
        sc = PatchCollection([PolygonPatch(p) for p in multipolygon.geoms])
        sc.set_color([0.95, 0.95, 0.95])  # light grey
        sc.set_edgecolor("k")
        axes.add_collection(sc, autolim=True)

    def plot_ship_contour_data(self):
        """Plots shipfile CONTOUR_DATA section"""
        try:
            xs = self.ship_class.contour_data.xqc
            ys = self.ship_class.contour_data.yqc
            xs.append(xs[0])
            ys.append(ys[0])
            plt.plot(xs, ys, "--r", label="contour_data")
        except AttributeError:
            warnings.warn("Error no contour_data was defined")

    def plot_echo_sounder_data(self):
        """Plots shipfile echo_sounder_data section"""
        try:
            x = self.ship_class.echo_sounder_data.xecho
            y = self.ship_class.echo_sounder_data.yecho
            plt.plot(x, y, "ob", label="Echo sounder sensor")
        except AttributeError:
            warnings.warn("Error no echo_sounder_data was defined")

    def plot_tunnel_thruster_data(self):
        """Plots shipfile tunnel_thruster_data section"""
        try:
            x = []
            y = []
            for tunnel in self.ship_class.tunnel_thruster_data:
                x.append(tunnel.xxtt)
                y.append(tunnel.yytt)
            plt.plot(x, y, "Xg", label="Tunnel thurster", markersize=10)
        except AttributeError:
            warnings.warn("Error no tunnel_thruster_data was defined")

    def plot_design_particulars_topview(self, cog=True, **kwargs):
        """Plots shipfile design_particulars section"""
        if cog:
            lcg = self.ship_class.design_particulars.lcg
            tcg = self.ship_class.design_particulars.tcg
            plt.plot(lcg, tcg, "+b", label="COG", markersize=15)

        # plot radius of gyrations
        kxxm = self.ship_class.design_particulars.kxxm
        kyym = self.ship_class.design_particulars.kyym
        kzzm = self.ship_class.design_particulars.kzzm
        lpp = self.ship_class.main_data.l
        beam = self.ship_class.main_data.beam

        x_pos = [0.1 * lpp, 0.1 * lpp]
        y_pos = [-kxxm, kxxm]
        label = "Roll radius of gyration"
        _plot_arrow(lpp, x_pos, y_pos, label, "-k", 0, 0.001, "k")

        x_pos = [-kyym, kyym]
        y_pos = [beam / 2 * 1.3, beam / 2 * 1.3]
        label = "Yaw radius of gyration"
        _plot_arrow(lpp, x_pos, y_pos, label, "--k", 0.001, 0, "k")

        x_pos = [-kzzm, kzzm]
        y_pos = [beam / 2 * 1.4, beam / 2 * 1.4]
        label = "Pitch radius of gyration"
        _plot_arrow(lpp, x_pos, y_pos, label, "-.k", 0.0001, 0, "k")

    def plot_main_data_topview(self):
        """Plots shipfile main_data section"""
        loa = self.ship_class.main_data.loa
        lpp = self.ship_class.main_data.l
        beam = self.ship_class.main_data.beam

        # Plot beam
        x_pos = [0.0 * lpp, 0.0 * lpp]
        y_pos = [-beam / 2, beam / 2]
        _plot_arrow(lpp, x_pos, y_pos, "Beam", "-b", 0, 0.001, "b", show_mid=False)

        # Plot LOA
        x_pos = [-loa / 2, loa / 2]
        y_pos = [beam / 2 * 1.1, beam / 2 * 1.1]
        _plot_arrow(lpp, x_pos, y_pos, "LOA", "-b", 0.0001, 0, "b", show_mid=False)

        # Plot LPP
        x_pos = [-lpp / 2, lpp / 2]
        y_pos = [beam / 2 * 1.2, beam / 2 * 1.2]
        _plot_arrow(lpp, x_pos, y_pos, "LPP", "--b", 0.0001, 0, "b", show_mid=False)

    def plot_winch_data(self):
        """Plots shipfile winch_data section"""
        try:
            x_pts = self.ship_class.winch_data.xkl
            y_pts = self.ship_class.winch_data.ykl
            pts = [(x, y) for x, y in zip(x_pts, y_pts)]

            # fmt: off
            for i, point in enumerate(pts):
                if i == 0:
                    plt.scatter(*point, c="yellow", s=80, linewidths=0.3,
                                edgecolors="black", label="Mooring fair lead")
                else:
                    plt.scatter(*point, c="yellow", s=80, linewidths=0.3, 
                                edgecolors="black")
                plt.annotate(str(i + 1), point, horizontalalignment="center",
                             verticalalignment="center", size=10)
            # fmt: on
        except KeyError:
            warnings.warn("Error no winch_data was defined")

    def plot_rudder_top_view(self, thickness_ratio=0.15, rudder_balance=0.25, **kwargs):
        # plot rudder profile on current axis seen from above
        # rudder_chord: rudder chord length (m)
        # thickness_ratio=0.15 NACA profile chord to thickness ratio (-)
        if len(self.ship_class.rudder_particulars) == 0:
            warnings.warn("Error no rudder was defined")
        for rudder in self.ship_class.rudder_particulars:
            rudder_chord = rudder.ar / rudder.rh  # approximation of rudder chord
            # relative postiotion of rudder stock from leading edge (relative to chord length)
            x = np.linspace(0, 1, 30)
            wing_x = -rudder_chord * x + rudder_balance * rudder_chord
            # fmt: off
            wing_y = (thickness_ratio / 0.2 * rudder_chord * 
                      (0.296 * np.sqrt(x) - 0.126 * x - 0.3516 * x**2 + 0.2843 * x**3 - 
                       0.1015 * x**4))
            # fmt: on
            # concatenate both sides of the rudder into one array
            wing_x = np.concatenate((wing_x, np.flip(wing_x)))
            wing_y = np.concatenate((wing_y, np.flip(-wing_y)))

            wing_x = wing_x + rudder.xxrud
            wing_y = wing_y + rudder.yyrud
            plt.plot(wing_x, wing_y, "b")

    def plot_propeller_top_view(self, hub_rel_diameter=0.15, **kwargs):
        """plot propeller profile on current axis seen from above
        hub_rel_diameter: hub diameter relative to propeller diameter (-)"""
        props = None
        if len(self.ship_class.fix_prop_data) > 0:
            props = self.ship_class.fix_prop_data
        if len(self.ship_class.cp_prop_data) > 0:
            props = self.ship_class.cp_prop_data
        if props is None:
            warnings.warn("No props data found")
            return

        for prop in props:
            propeller_xpos = prop.xxcp if hasattr(prop, "xxcp") else prop.xxfix
            propeller_ypos = prop.yycp if hasattr(prop, "xxcp") else prop.yyfix
            propeller_diameter = prop.dcp if hasattr(prop, "xxcp") else prop.dfix
            hub_diameter = propeller_diameter * hub_rel_diameter

            blade_top_x, blade_top_y, blade_bottom_x, blade_bottom_y, b = _get_blade(
                propeller_xpos, propeller_ypos, propeller_diameter, hub_diameter
            )
            hub_x, hub_z = _get_hub(propeller_xpos, propeller_ypos, hub_diameter, b)

            plt.plot(blade_top_x, blade_top_y, "b")
            plt.plot(blade_bottom_x, blade_bottom_y, "b")
            plt.plot(hub_x, hub_z, "b")

    # fmt: off
    def plot_top_view(self, contour=True, contour_data=True,
                      design_particulars=True, main_data=True, sounders=True,
                      thruster=True, whinch=True, rudder=True, propeller=True, 
                      hub_rel_diameter=0.15, thickness_ratio=0.2, rudder_balance=0.25,
                      **kwargs):
        # fmt: on
        fig, axes = plt.subplots(constrained_layout=True)
        fig.set_size_inches(17, 7)
        axes.set_aspect("equal", "box")
        if contour:
            self.plot_ship_plot_contour(axes)
        if contour_data:
            self.plot_ship_contour_data()
        if design_particulars:
            self.plot_design_particulars_topview(**kwargs)
        if main_data:
            self.plot_main_data_topview()
        if sounders:
            self.plot_echo_sounder_data()
        if thruster:
            self.plot_tunnel_thruster_data()
        if whinch:
            self.plot_winch_data()
        if rudder:
            self.plot_rudder_top_view(**kwargs)
        if propeller:
            self.plot_propeller_top_view(**kwargs)
        plt.legend(fancybox=True, framealpha=0.1, 
                   loc='upper left', bbox_to_anchor=(0., -0.1), ncol=2)
        plt.xlabel("Axial position relative Lpp/2 [m]")
        plt.ylabel("Lateral position relative centerline [m]")
        axes.margins(y=0.05)
        axes.invert_yaxis()
        plt.grid(True)
        save_file_name = "top_view.png"
        fig.savefig(os.path.join(self.save_path, save_file_name))


class SideView:
    # fmt: off
    def __init__(self, shipdict: dict, save_path, 
                 default_side_contour = np.array(
            [[-78.89, 18.44], [-72.97, 18.55], [-71.89, 33.80], [-72.73, 34.91],
             [-67.52, 33.99], [-65.24, 23.25], [-65.21, 26.05], [-63.11, 26.05],
             [-63.16, 28.76], [-59.61, 28.76], [-59.61, 29.76], [-60.27, 32.26],
             [-60.77, 32.26], [-60.46, 32.71], [-57.21, 32.76], [-56.85, 33.13],
             [-56.52, 33.26], [-56.58, 40.92], [-56.34, 40.96], [-56.30, 33.26],
             [-48.34, 33.26], [-47.98, 32.26], [-48.97, 29.43], [-48.16, 18.40],
             [-42.76, 18.56], [-35.48, 14.33], [44.96, 14.15], [54.00, 18.65],
             [67.50, 19.15], [67.50, 28.00], [68.00, 28.00], [68.00, 19.17],
             [79.92, 19.48], [76.12, 9.37], [77.80, 8.99], [79.97, 7.81], [80.54, 6.21],
             [80.54, 5.02], [79.70, 3.34], [76.75, 1.42], [71.18, 0.00], [67.98, 0.00],
             [-64.07, 0.00], [-65.45, 0.00], [-66.88, 0.00], [-68.47, 1.42],
             [-69.26, 2.03], [-70.16, 2.69], [-70.05, 3.79], [-69.26, 4.25],
             [-68.99, 4.81], [-68.97, 5.86], [-69.10, 6.31], [-69.49, 6.86],
             [-70.22, 7.41], [-71.91, 8.00], [-72.74, 8.02], [-73.25, 6.82],
             [-78.23, 6.82], [-78.71, 9.03], [-78.89, 18.40], [-78.89, 18.44],
            ]
        )) -> None:
        # fmt: on
        self.shipdict = shipdict
        self.ship_class = get_ShipFile(shipdict)
        self.save_path = save_path
        self.default_contour = default_side_contour
        self.defult_l = 159
        self.default_d = 10

    def scale_model(self) -> list:
        avg_draught = self._get_avg_draught()
        loa = self.ship_class.main_data.loa
        scaled_m = []
        for x, z in self.default_contour:
            scaled_m.append([x / self.defult_l * loa, z / self.default_d * avg_draught])
        return scaled_m

    def _get_avg_draught(self):
        design_particulars = self.ship_class.design_particulars
        avg_draught = (design_particulars.ta + design_particulars.tf) / 2
        return avg_draught

    def plot_contour(self, axes):
        side_cont = self.scale_model()
        polygons = [Polygon(side_cont)]
        multipolygon = MultiPolygon(polygons)

        print(multipolygon.geoms)
        sc = PatchCollection([PolygonPatch(p) for p in multipolygon.geoms])
        sc.set_color([0.95, 0.95, 0.95])  # light grey
        sc.set_edgecolor("k")
        axes.add_collection(sc, autolim=True)

    def plot_rudder(self, rudder_balance=0.25, **kwargs):
        """plots the side view of the rudder"""
        for rudder in self.ship_class.rudder_particulars:
            rudder_xpos = rudder.xxrud
            rudder_zpos = rudder.zzrud - rudder.rh * 0.5
            rudder_area = rudder.ar
            rudder_height = rudder.rh
            rudder_chord = rudder_area / rudder_height

            wing_x = np.array([0, -rudder_chord, -rudder_chord, 0, 0])
            wing_z = np.array([0, 0, -rudder_height, -rudder_height, 0])

            wing_x = wing_x + rudder_xpos + rudder_chord * rudder_balance
            wing_z = wing_z + -rudder_zpos
            plt.plot(wing_x, wing_z, "b")

    def plot_prop(self, hub_rel_diameter: float = 0.25):
        props = None
        if len(self.ship_class.fix_prop_data) > 0:
            props = self.ship_class.fix_prop_data
        if len(self.ship_class.cp_prop_data) > 0:
            props = self.ship_class.cp_prop_data
        if props is None:
            warnings.warn("No props data found")
            return

        for prop in props:
            propeller_xpos = prop.xxcp if hasattr(prop, "xxcp") else prop.xxfix
            propeller_zpos = -prop.zzcp if hasattr(prop, "xxcp") else -prop.zzfix
            propeller_diameter = prop.dcp if hasattr(prop, "xxcp") else prop.dfix
            hub_diameter = propeller_diameter * hub_rel_diameter

            blade_top_x, blade_top_z, blade_bottom_x, blade_bottom_z, b = _get_blade(
                propeller_xpos, propeller_zpos, propeller_diameter, hub_diameter
            )
            hub_x, hub_z = _get_hub(propeller_xpos, propeller_zpos, hub_diameter, b)

            plt.plot(blade_top_x, blade_top_z, "b")
            plt.plot(blade_bottom_x, blade_bottom_z, "b")
            plt.plot(hub_x, hub_z, "b")

    def plot_tunnel_thruster_data(self):
        """Plots shipfile tunnel_thruster_data section"""
        x = []
        z = []
        for tunnel in self.ship_class.tunnel_thruster_data:
            x.append(tunnel.xxtt)
            z.append(-tunnel.zztt)
        plt.plot(x, z, "Xg", label="Tunnel thurster", markersize=10)

    def plot_whinches(self):
        if self.ship_class.winch_data.zkl is None:
            warnings.warn("No zkl was found for the whinches")
            return
        if len(self.ship_class.winch_data.zkl) == 0:
            warnings.warn("No zkl was found for the whinches")
            return
        x_pts = self.ship_class.winch_data.xkl
        z_pts = self.ship_class.winch_data.zkl
        pts = [(x, -z) for x, z in zip(x_pts, z_pts)]

        for i, point in enumerate(pts):
            if i == 0:
                plt.scatter(
                    *point,
                    c="yellow",
                    s=80,
                    linewidths=0.3,
                    edgecolors="black",
                    label="Mooring fair lead",
                )
            else:
                plt.scatter(
                    *point, c="yellow", s=80, linewidths=0.3, edgecolors="black"
                )
            plt.annotate(
                str(i + 1),
                point,
                horizontalalignment="center",
                verticalalignment="center",
                size=10,
            )

    def plot_cog(self):
        lcg = self.ship_class.design_particulars.lcg
        kg = self.ship_class.design_particulars.kg
        plt.plot(lcg, kg, "+b", label="COG", markersize=15)

    def plot_draught_arrows(self):
        ta = self.ship_class.design_particulars.ta
        tf = self.ship_class.design_particulars.tf
        end_pos = -self.ship_class.main_data.loa / 2
        xs = [-end_pos * 1.1, -end_pos * 1.1]
        loa = self.ship_class.main_data.loa
        _plot_arrow(loa, xs, [tf, 0], f"Draught fwd: {tf}", "--", 0, -0.001, "b")
        xs = [end_pos * 1.1, end_pos * 1.1]
        _plot_arrow(loa, xs, [ta, 0], f"Draught aft: {ta}", "--", 0, -0.001, "b")

    def plot_wind_area(self):
        al = self.ship_class.wind_data.al
        loa = self.ship_class.main_data.loa
        height = float(al) / float(loa)
        x = np.array([loa / 2, loa / 2, -loa / 2, -loa / 2, loa / 2])
        z = np.array([height, 0, 0, height, height])
        z += self._get_avg_draught()
        plt.plot(x, z, "--r", label="Wind area")

    # fmt: off
    def plot_side_view(self, contour=True, rudder=True, propeller=True, thruster=True, 
                       cog=True, whinch=True, draught_arrows=True, wind_area=True, 
                       **kwargs):
        # fmt: on
        fig, axes = plt.subplots(constrained_layout=True)
        fig.set_size_inches(17, 7)
        axes.set_aspect("equal", "box")
        if contour:
            self.plot_contour(axes)
        if rudder:
            self.plot_rudder(**kwargs)
        if propeller:
            self.plot_prop(**kwargs)
        if thruster:
            self.plot_tunnel_thruster_data()
        if cog:
            self.plot_cog()
        if whinch:
            self.plot_whinches()
        if draught_arrows:
            self.plot_draught_arrows()
        if wind_area:
            self.plot_wind_area()
        plt.xlabel("Axial position relative Lpp/2 [m]")
        plt.ylabel("Axial position relative to baseline [m]")
        axes.margins(y=0.05)
        axes.margins(x=0.05)
        plt.legend(fancybox=True, framealpha=0.1, 
                   loc='upper left', bbox_to_anchor=(0., -0.1), ncol=2)
        plt.grid(True)
        save_file_name = "side_view.png"
        fig.savefig(os.path.join(self.save_path, save_file_name))


def plot_views(shipdict, store_path, **kwargs):
    if "anchor_data" in shipdict:
        try:
            shipdict["anchor_data"] = shipdict["anchor_data"][0]
        except:
            pass
    side_view = SideView(shipdict, store_path)
    side_view.plot_side_view(**kwargs)
    top_view = TopView(shipdict, store_path)
    top_view.plot_top_view(**kwargs)


if __name__ == "__main__":
    THIS_DIR = os.path.dirname(__file__)
    ship_path = os.path.join(THIS_DIR, "test_ship.ship")
    ship_dict = json.loads(open(ship_path).read())
    plot_views(ship_dict, "", hub_rel_diameter=0.25, rudder=True)
