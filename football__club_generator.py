import xml.etree.ElementTree as ET
import os
import random as rnd


def generator_interface(path):
    og_dir = os.getcwd()
    os.chdir(path)
    print("Hello and welcome in the club generator interface !\n")
    str_name = input("First of all type the name of the club here: ")
    root = ET.Element("club")
    name_node = ET.SubElement(root, "name")
    name_node.text = str_name

    country_node = ET.SubElement(root, "country")
    country_node.text = "dummy country"
    tier_node = ET.SubElement(root, "tier")
    tier_node.text = "0"
    pot_node = ET.SubElement(root, "pot")
    pot_node.text = "0"

    tact_node = ET.SubElement(root, "tactic")
    w_node = ET.SubElement(tact_node, "weight")
    w_node.text = "1.0"
    nb_df = input("Number of defenders used by the main tactic: ")
    nb_mid = input("Number of midfielders used by the main tactic: ")
    nb_fw = input("Number of forwards used by the main tactic: ")
    formation_node = ET.SubElement(tact_node, "formation")
    formation_node.text = nb_df+"-"+nb_mid+"-"+nb_fw

    avg = int(input("Enter the average strength of a team's player here: "))
    var = float(input("Enter the variance around the team's player strength here: "))
    cum_strength = 0

    for i in range(2*(1+int(nb_df)+int(nb_mid)+int(nb_fw))):
        current_player = ET.SubElement(root, "player")
        player_name = ET.SubElement(current_player, "name")
        player_name.text = str_name+"_"+str(i)
        player_nat = ET.SubElement(current_player, "country")
        player_nat.text = "dummy country"
        adjusted_avg = ((avg*2*(1+int(nb_df)+int(nb_mid)+int(nb_fw))) - cum_strength) /\
                       (2*(1+int(nb_df)+int(nb_mid)+int(nb_fw))-i)
        strength = int(rnd.normalvariate(adjusted_avg, var))
        player_str = ET.SubElement(current_player, "strength")
        if i < 2:
            player_str.text = str(strength)
            player_pen = ET.SubElement(current_player, "pen_shooter")
            player_pen.text = str(False)
            player_gk = ET.SubElement(current_player, "gk_ability")
            player_gk.text = str(1.0)
            player_df = ET.SubElement(current_player, "df_ability")
            player_df.text = str(0.0)
            player_md = ET.SubElement(current_player, "md_ability")
            player_md.text = str(0.0)
            player_fw = ET.SubElement(current_player, 'fw_ability')
            player_fw.text = str(0.0)
        elif i < 2*(1+int(nb_df)):
            player_str.text = str(strength)
            player_pen = ET.SubElement(current_player, "pen_shooter")
            player_pen.text = str(False)
            player_gk = ET.SubElement(current_player, "gk_ability")
            player_gk.text = str(0.0)
            player_df = ET.SubElement(current_player, "df_ability")
            player_df.text = str(1.0)
            player_md = ET.SubElement(current_player, "md_ability")
            md_ability = rnd.random()
            if (md_ability < 0.5) or (md_ability > 0.95):
                md_ability = 0.0
            player_md.text = str(md_ability)
            player_fw = ET.SubElement(current_player, 'fw_ability')
            player_fw.text = str(0.0)
        elif i < 2*(1+int(nb_df)+int(nb_mid)):
            player_str.text = str(strength)
            player_pen = ET.SubElement(current_player, "pen_shooter")
            pen_taker = rnd.random() > 0.8
            player_pen.text = str(pen_taker)
            player_gk = ET.SubElement(current_player, "gk_ability")
            player_gk.text = str(0.0)
            player_df = ET.SubElement(current_player, "df_ability")
            df_ability = rnd.random()
            if (df_ability < 0.5) or (df_ability > 0.95):
                df_ability = 0.0
            player_df.text = str(df_ability)
            player_md = ET.SubElement(current_player, "md_ability")
            player_md.text = str(1.0)
            player_fw = ET.SubElement(current_player, 'fw_ability')
            fw_ability = rnd.random()
            if (fw_ability < 0.5) or (fw_ability > 0.95):
                fw_ability = 0.0
            player_fw.text = str(fw_ability)
        else:
            if i == 2*(1+int(nb_df)+int(nb_mid)+int(nb_fw))-1:
                target_strength = 2*(1+int(nb_df)+int(nb_mid)+int(nb_fw))*avg
                strength = target_strength-cum_strength
            player_str.text = str(strength)
            player_pen = ET.SubElement(current_player, "pen_shooter")
            pen_taker = rnd.random() > 0.4
            player_pen.text = str(pen_taker)
            player_gk = ET.SubElement(current_player, "gk_ability")
            player_gk.text = str(0.0)
            player_df = ET.SubElement(current_player, "df_ability")
            player_df.text = str(0.0)
            player_md = ET.SubElement(current_player, "md_ability")
            md_ability = rnd.random()
            if (md_ability < 0.5) or (md_ability > 0.95):
                md_ability = 0.0
            player_md.text = str(md_ability)
            player_fw = ET.SubElement(current_player, 'fw_ability')
            player_fw.text = str(1.0)
        cum_strength += strength
    tree = ET.ElementTree(root)
    tree.write(str_name.upper()+".xml")
    os.chdir(og_dir)