from dataclasses import dataclass
from typing import Optional, List

from dacite import from_dict, Config

class Subgroups:
    """A wrapper class holding all sub elements of the ship file with all parameters of
    the sub element etc.
    """

    @dataclass
    class added_mass_coeff_data:
        kpd: Optional[float]
        nrd: Optional[float]
        xud: Optional[float]
        yvd: Optional[float]

    @dataclass
    class _anchor:
        dcab: Optional[float]
        lcabtot: Optional[float]
        pwwl: Optional[float]
        wanc: Optional[float]
        wcbl: Optional[float]
        wlrmax: Optional[float]
        xanh: Optional[float]
        yanh: Optional[float]
        zanh: Optional[float]

    @dataclass
    class anchor_data(list[_anchor]):
        pass

    @dataclass
    class ap_data:
        a_ship: Optional[float]
        pid_td: Optional[float]
        pid_kp: Optional[float]
        rref1: Optional[float]
        pid_ti: Optional[float]

    @dataclass
    class _azimuth:
        azr: Optional[float]
        nazdm: Optional[float]
        pdaz: Optional[float]
        daz: Optional[float]
        xxaz: Optional[float]
        yyaz: Optional[float]
        zzaz: Optional[float]

    @dataclass
    class azimuth_data(list[_azimuth]):
        pass

    @dataclass
    class bollards:
        xkl: Optional[list]
        ykl: Optional[list]
        zkl: Optional[list]

    @dataclass
    class combinator:
        jdpset: Optional[list]
        nset: Optional[list]
        pdfset: Optional[list]
        pdset: Optional[list]

    @dataclass
    class contour_data:
        xqc: Optional[list]
        yqc: Optional[list]

    @dataclass
    class _fix_prop:
        dfix: Optional[float]
        gearfix: Optional[float]
        pdfix: Optional[float]
        protfix: Optional[float]
        tdffix: Optional[float]
        wffix: Optional[float]
        eta_r: Optional[float]
        xxfix: Optional[float]
        yyfix: Optional[float]
        zzfix: Optional[float]

    @dataclass
    class fix_prop_data(list[_fix_prop]):
        pass

    @dataclass
    class _cp_prop:
        blade_area: Optional[float]
        dcp: Optional[float]
        gearcp: Optional[float]
        pdcp: Optional[float]
        protcp: Optional[float]
        tdfcp: Optional[float]
        wfcp: Optional[float]
        xxcp: Optional[float]
        yycp: Optional[float]
        z: Optional[float]
        zzcp: Optional[float]

    @dataclass
    class cp_prop_data(list[_cp_prop]):
        pass

    @dataclass
    class design_particulars:
        a0: Optional[float]
        askeg: Optional[float]
        bblk: Optional[float]
        bk: Optional[float]
        br: Optional[float]
        bra: Optional[float]
        disp: Optional[float]
        gm: Optional[float]
        kg: Optional[float]
        kxxm: Optional[float]
        kyym: Optional[float]
        kzzm: Optional[float]
        lblk: Optional[float]
        lcg: Optional[float]
        slag: Optional[float]
        ta: Optional[float]
        tcg: Optional[float]
        tf: Optional[float]
        ud: Optional[float]

    @dataclass
    class _engine:
        accteng: Optional[float]
        fuel100: Optional[float]
        fuel25: Optional[float]
        fuel50: Optional[float]
        fuel75: Optional[float]
        igen: Optional[float]
        imeng: Optional[float]
        kpe: Optional[float]
        nengmin: Optional[float]
        nnom: Optional[float]
        pbeng: Optional[float]
        qchar: Optional[list]

    @dataclass
    class _adv_engine:
        Mact: Optional[float]
        Phigh: Optional[float]
        Plow: Optional[float]
        Tact: Optional[float]
        Taud: Optional[float]
        Vold: Optional[float]
        cfric: Optional[float]
        cfriceng: Optional[float]
        dg1: Optional[float]
        fpimx: Optional[list]
        fpr: Optional[list]
        gfr: Optional[list]
        ig2: Optional[float]
        pg1: Optional[float]
        revlim: Optional[float]
        rpmllc: Optional[list]
        vt0: Optional[float]

    @dataclass
    class diesel_engine_data(list[_engine, _adv_engine]):
        pass

    @dataclass
    class dolph_data:
        kdol: Optional[float]
        mydol: Optional[float]
        nydol: Optional[float]

    @dataclass
    class echo_sounder_data:
        xecho: Optional[list]
        yecho: Optional[list]

    @dataclass
    class isherwood_data:
        ass: Optional[float]
        c: Optional[float]
        m: Optional[float]
        sw: Optional[float]

    @dataclass
    class lin_hull_coeff_data:
        kp: Optional[float]
        kpap: Optional[float]
        krar: Optional[float]
        kup: Optional[float]
        kur: Optional[float]
        kuur: Optional[float]
        kuuv: Optional[float]
        kuv: Optional[float]
        kvav: Optional[float]
        nur: Optional[float]
        nuuf: Optional[float]
        nuur: Optional[float]
        nuuv: Optional[float]
        nuv: Optional[float]
        slev: Optional[float]
        yur: Optional[float]
        yuur: Optional[float]
        yuuv: Optional[float]
        yuv: Optional[float]

    @dataclass
    class linecon_points(list):
        pass

    @dataclass
    class main_data:
        beam: Optional[float]
        height: Optional[float]
        l: Optional[float]
        loa: Optional[float]
        ndof: Optional[float]
        shiptype: Optional[float]
        ship_type_name: Optional[str]
        steerarr: Optional[float]
        thrustrarr: Optional[float]
        height: Optional[float]

    @dataclass
    class max_rates:
        ndm: Optional[float]
        pdm: Optional[float]

    @dataclass
    class name(str):
        pass

    @dataclass
    class non_lin_coeff_data:
        cd: Optional[float]
        cdnc: Optional[float]
        cdyc: Optional[float]
        unllim: Optional[float]

    @dataclass
    class _p1:
        pdh: Optional[float]
        pds: Optional[float]

    @dataclass
    class _p2:
        pdl: Optional[list]
        pdr: Optional[list]

    @dataclass
    class pitch_servo_data(list[_p1, _p2]):
        pass

    @dataclass
    class plot_contour(list):
        pass

    @dataclass
    class pod_data(list):
        pass

    @dataclass
    class prop_char:
        jktpos: Optional[float]
        ktpos: Optional[float]
        jktneg: Optional[float]
        ktneg: Optional[float]
        jkqpos: Optional[float]
        kqpos: Optional[float]
        jkqneg: Optional[float]
        kqneg: Optional[float]

    @dataclass
    class _prop_coeffs1:
        ckqhead: Optional[float]
        ckqstern: Optional[float]
        ckthead: Optional[float]
        cktstern: Optional[float]
        cstn: Optional[float]
        pdcorr: Optional[float]

    @dataclass
    class _prop_coeffs2:
        ktyh: Optional[float]
        ktys: Optional[float]

    @dataclass
    class propeller_coeff_data(list[_prop_coeffs1, _prop_coeffs2]):
        pass

    @dataclass
    class _jet:
        pjr: Optional[float]
        npjdm: Optional[float]
        pdpj: Optional[float]
        npjd: Optional[float]
        xxpj: Optional[float]
        yypj: Optional[float]
        zzpj: Optional[float]

    @dataclass
    class pump_jet_data(list[_jet]):
        pass

    @dataclass
    class quay_data:
        kquay: Optional[float]
        myq: Optional[float]
        nyq: Optional[float]
        redfac: Optional[float]

    @dataclass
    class res_data:
        res: Optional[list]
        vres: Optional[list]

    @dataclass
    class res_shallow_data:
        fnhr: Optional[list]
        sres1: Optional[list]
        sres2: Optional[list]
        sres3: Optional[list]
        sres4: Optional[list]
        sres5: Optional[list]

    @dataclass
    class resistance_data:
        r100d: Optional[float]
        r25d: Optional[float]
        r50d: Optional[float]
        r75d: Optional[float]
        rcors: Optional[float]
        xrr: Optional[float]
        xvr: Optional[float]
        xvv: Optional[float]

    @dataclass
    class rudder_coeff_data:
        kr: Optional[float]
        kv: Optional[float]
        s: Optional[float]
        slask1: Optional[float]
        slask2: Optional[float]
        xyrd: Optional[float]
        ytd: Optional[float]
        yuud: Optional[float]
        yuuds: Optional[float]

    @dataclass
    class _rudder_par:
        ar: Optional[float]
        arh: Optional[float]
        delopt: Optional[float]
        irudprop: Optional[float]
        maxhelm: Optional[float]
        maxhext: Optional[float]
        rh: Optional[float]
        rr: Optional[float]
        rudtype: Optional[float]
        xxrud: Optional[float]
        yyrud: Optional[float]
        zzrud: Optional[float]

    @dataclass
    class rudder_particulars(list[_rudder_par]):
        pass

    @dataclass
    class section_coord_data:
        noOfSections: Optional[float]
        dlsec: Optional[float]
        zbl: Optional[float]
        np: Optional[list]
        coordinates: Optional[dict]

    @dataclass
    class section_data:
        asec: Optional[list]
        bsec: Optional[list]
        tsec: Optional[list]

    @dataclass
    class shallow_water_coeff:
        cdz: Optional[float]
        nurzc: Optional[float]
        nuvzc: Optional[float]
        yurzc: Optional[float]
        yuvzc: Optional[float]

    @dataclass
    class ship_interaction:
        cnmt: Optional[float]
        cymt: Optional[float]
        int_type: Optional[float]

    @dataclass
    class _thruster:
        accttt: Optional[float]
        pdtt: Optional[float]
        ttcorr: Optional[float]
        ttt: Optional[float]
        xxtt: Optional[float]
        yytt: Optional[float]
        zztt: Optional[float]

    @dataclass
    class tunnel_thruster_data(list[_thruster]):
        pass

    @dataclass
    class voith_data:
        []

    @dataclass
    class wave_coeff_data:
        cfal: Optional[float]

    @dataclass
    class winch_data:
        cwir: Optional[float]
        fwhm: Optional[float]
        fwm: Optional[float]
        wblo: Optional[float]
        winm: Optional[list]
        winr: Optional[float]
        xkl: Optional[list]
        ykl: Optional[list]
        zkl: Optional[list]

    @dataclass
    class wind_coeff:
        ckin: Optional[list]
        cnin: Optional[list]
        cxin: Optional[list]
        cyin: Optional[list]

    @dataclass
    class wind_data:
        al: Optional[float]
        at: Optional[float]
        wcat: Optional[float]


@dataclass
class ShipFile:
    """A wrapper class holding all subgroups of the ship file"""

    added_mass_coeff_data: Subgroups.added_mass_coeff_data
    anchor_data: Subgroups.anchor_data
    ap_data: Subgroups.ap_data
    azimuth_data: Subgroups.azimuth_data
    bollards: Subgroups.bollards
    combinator: Subgroups.combinator
    contour_data: Subgroups.contour_data
    fix_prop_data: Subgroups.fix_prop_data
    cp_prop_data: Subgroups.cp_prop_data
    design_particulars: Subgroups.design_particulars
    diesel_engine_data: Subgroups.diesel_engine_data
    dolph_data: Subgroups.dolph_data
    echo_sounder_data: Subgroups.echo_sounder_data
    isherwood_data: Subgroups.isherwood_data
    lin_hull_coeff_data: Subgroups.lin_hull_coeff_data
    linecon_points: Subgroups.linecon_points
    main_data: Subgroups.main_data
    max_rates: Subgroups.max_rates
    name: Subgroups.name
    non_lin_coeff_data: Subgroups.non_lin_coeff_data
    pitch_servo_data: Subgroups.pitch_servo_data
    plot_contour: Subgroups.plot_contour
    prop_char: Subgroups.prop_char
    propeller_coeff_data: Subgroups.propeller_coeff_data
    pump_jet_data: Subgroups.pump_jet_data
    quay_data: Subgroups.quay_data
    res_data: Subgroups.res_data
    res_shallow_data: Subgroups.res_shallow_data
    resistance_data: Subgroups.resistance_data
    rudder_coeff_data: Subgroups.rudder_coeff_data
    rudder_particulars: Subgroups.rudder_particulars
    section_coord_data: Subgroups.section_coord_data
    section_data: Subgroups.section_data
    shallow_water_coeff: Subgroups.shallow_water_coeff
    ship_interaction: Subgroups.ship_interaction
    tunnel_thruster_data: Subgroups.tunnel_thruster_data
    voith_data: Subgroups.voith_data
    wave_coeff_data: Subgroups.wave_coeff_data
    winch_data: Subgroups.winch_data
    wind_coeff: Subgroups.wind_coeff
    wind_data: Subgroups.wind_data



def get_ShipFile(shipdict: dict, print_error=False) -> ShipFile:
    """Loops over the ShipFile and Subgroups to create a ShipFile dataclass containg the
    same information as the shipdict but instead of getting the loa from the shipdict
    like this shipdict["main_data"]["loa"] you can use ship_file.main_data.loa, each
    group / subgroup can also be autocompleted in vscode.

    Args:
        shipdict (dict): the dictonary of dictonaries containg the ship information
        print_error (bool, optional): If you want to see potential errors.
            Defaults to False.

    Returns:
        ShipFile: the shipdict as a dataclass
    """

    @dataclass
    class SF:
        pass

    sf = SF()
    conf = Config(check_types=False)
    for key in shipdict.keys():
        try:
            sys = from_dict(getattr(Subgroups, key), shipdict[key])
            if hasattr(sys, "append"):
                for sub in shipdict[key]:
                    if hasattr(sys, "__orig_bases__"):
                        sub_class_name = str(sys.__orig_bases__[0]).split(".")[-1][:-1]
                        sub_class = getattr(Subgroups, sub_class_name)
                        sub_sys = from_dict(sub_class, sub)
                        sys.append(sub_sys)
                    else:
                        sys.append(sub)
        except Exception as e:
            if print_error:
                print(e)
            try:
                sys = from_dict(getattr(Subgroups, key), shipdict[key], conf)
            except Exception as e:
                if print_error:
                    print(e)
                sys = None
        if key == "name":
            sys = shipdict[key]
        sf.__setattr__(key, sys)
    return sf
