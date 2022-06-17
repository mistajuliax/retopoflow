'''
Patrick Moore
Modify this file to change you default keymap for contours

Events reported at 'CTRL+SHIFT+ALT+TYPE'
eg.   'CTRL+SHIFT+A' is a valid event but 'SHIFT+CTRL+A' is not

For a list of available key types, see
http://www.blender.org/documentation/blender_python_api_2_70a_release/bpy.types.Event.html?highlight=event.type#bpy.types.Event.type

DO NOT REMOVE ANY ITEMS from the default key_maps
If you want an item unmapped, do it as follows
def_cs_map['example_op'] = {}

Decent Resrouces:
#http://www.blender.org/documentation/blender_python_api_2_70a_release/bpy.types.KeyMapItem.html
#http://www.blender.org/documentation/blender_python_api_2_70a_release/bpy.types.KeyMap.html
#http://www.blender.org/documentation/blender_python_api_2_70a_release/bpy.types.KeyConfig.html
http://blender.stackexchange.com/questions/4832/how-to-find-the-right-keymap-to-change-on-addon-registration
'''


import bpy

def_rf_key_map = {
    'action': {'LEFTMOUSE'},
    'select': {'LEFTMOUSE'},
    'select all': {'A'},
    'cancel': {'ESC', 'CTRL+ALT+DEL'},
    'confirm': {'RET', 'NUMPAD_ENTER'},
    'modal confirm': {'SPACE', 'RET', 'NUMPAD_ENTER'},
    'modal cancel': {'RIGHTMOUSE', 'ESC'},
    'modal precise': 'SHIFT',
    'modal constrain': 'ALT',
    'scale': {'S'},
    'translate': {'G'},
    'rotate': {'R'},
    'delete': {'X', 'DEL'},
    'view cursor': {'C'},
    'undo': {'CTRL+Z'},
    'help': {'SHIFT+SLASH'},
    'snap cursor': {'SHIFT+S'},
    'navigate': set(),
    'up count': {'SHIFT+NUMPAD_PLUS', 'SHIFT+WHEELUPMOUSE'},
    'dn count': {'SHIFT+NUMPAD_MINUS', 'SHIFT+WHEELDOWNMOUSE'},
    'bridge': {'B'},
    'new': {'N'},
    'align': {'SHIFT+A', 'CRTL+A', 'ALT+A'},
    'up shift': {'LEFT_ARROW'},
    'dn shift': {'RIGHT_ARROW'},
    'mode': {'TAB'},
    'brush size': {'F'},
    'change junction': {'CTRL+C'},
    'dissolve': {'CTRL+D'},
    'fill': {'SHIFT+F'},
    'knife': {'K'},
    'merge': {'M'},
    'rip': {'CTRL+R'},
    'rotate pole': {'R', 'SHIFT+R'},
    'scale handles': {'CTRL+S'},
    'smooth': {'C'},
    'tweak move': {'T'},
    'tweak relax': {'SHIFT+T'},
    'update': {'CTRL+U'},
    'zip': {'Z'},
    'zip down': {'CTRL+NUMPAD_PLUS'},
    'zip up': {'CTRL+NUMPAD_MINUS'},
}

navigation_events = {
    'Move View',
    'Zoom View',
    'View Pan',
    'View Orbit',
    'Rotate View',
    'View Persp/Ortho',
    'View Numpad',
    'NDOF Orbit View',
    'NDOF Pan View',
    'View Selected',
    'Center View to Cursor',
}

def get_nav_keys(keycon):
    nav_keys = set()
    if '3D View' not in keycon.keymaps:
        print(keycon.name)
        for km in keycon.keymaps:
            print(km.name)
        print('Your keyconfig has no 3D view keymap, please email developer')
        return nav_keys
    
    #navigation keys last, to avoid conflicts eg, Ctl + Wheel
    #center view on cursor is included in nav
    for kmi in keycon.keymaps['3D View'].keymap_items:
        if kmi.name in navigation_events:    
            nav_keys.add(kmi_details(kmi))
                
    #bug, WHEELOUTMOUSE and WHEELINMOUSE used in 3dview keymaap
    nav_keys.add('WHEELDOWNMOUSE')
    nav_keys.add('WHEELUPMOUSE')
    
    return nav_keys

def kmi_details(kmi):
    kmi_ctrl    = 'CTRL+'  if kmi.ctrl  else ''
    kmi_shift   = 'SHIFT+' if kmi.shift else ''
    kmi_alt     = 'ALT+'   if kmi.alt   else ''
    return kmi_ctrl + kmi_shift + kmi_alt + kmi.type
    

#if 'Blender User' in bpy.context.window_manager.keyconfigs:
#    print('Blender User Key Config')
#    def_rf_key_map['navigate'] = get_nav_keys(bpy.context.window_manager.keyconfigs['Blender User'])
#else:
#    print('Blender Key Config')
#    def_rf_key_map['navigate'] = get_nav_keys(bpy.context.window_manager.keyconfigs['Blender'])



       
def find_kmi_by_idname(idname, keymap = None, keycon = None):
    
    if not keycon:
        C = bpy.context
        wm = C.window_manager
        if 'Blender User' in wm.keyconfigs:
            keycon = wm.keyconfigs['Blender User']
        else:
            keycon = wm.keyconfigs.active

    kmis = []

    keymaps = [keycon.keymaps[keymap]] if keymap else keycon.keymaps
    for km in keymaps:
        kmis.extend(
            kmi_details(kmi) for kmi in km.keymap_items if kmi.idname == idname
        )

    return kmis

    
def add_to_dict(km_dict, key,value, safety = True):   
    if safety:
        for k in km_dict.keys():
            if value in km_dict[k]:
                print('%s is already part of keymap "%s"' % (value, key))
                if key not in km_dict:
                    km_dict[key] = {}
                return False

    if key in km_dict:
        val = km_dict[key]

        if value in val:
            return False
        val.add(value)
    else:
        km_dict[key] = {value}

    return True
       
def rtflow_default_keymap_generate():
    km_dict = def_rf_key_map.copy()
    
    #bug, WHEELOUTMOUSE and WHEELINMOUSE used in 3dview keymap
    add_to_dict(km_dict,'navigate', 'WHEELUPMOUSE')
    add_to_dict(km_dict,'navigate', 'WHEELDOWNMOUSE')
    
    for kmi in bpy.context.window_manager.keyconfigs['Blender'].keymaps['3D View'].keymap_items:
        if kmi.name in navigation_events:     
            add_to_dict(km_dict,'navigate',kmi_details(kmi))
    return km_dict
          
          
def rtflow_keymap():
    '''
    this is a dynamic attempt to generate key map.  Buggy, unpredictable and no very useful
    '''
    C = bpy.context
    wm = C.window_manager
    if 'Blender User' in wm.keyconfigs:
        keycon = wm.keyconfigs['Blender User']
    else:
        keycon = wm.keyconfigs.active

    if '3D View' not in keycon.keymaps:
        print(keycon.name)
        print('you have no 3D View config in your keymap, reverting to default Blender')
        keycon = wm.keyconfigs['Blender']
    #get a backup, default keymap (which can be edited by user for overrides)
    #TODO make the defaults for these better
    if 'maya' in keycon.name:
        def_map = def_rf_key_map
    def_map = def_rf_key_map
    #Attempt to gather user preferred actions from Blender prefs    
    sel = C.user_preferences.inputs.select_mouse
    sel += 'MOUSE'

    act = def_rf_key_map['action']
    nav_keys = get_nav_keys(keycon)
    km_dict = {
        'cancel': def_rf_key_map['cancel'],
        'confirm': def_rf_key_map['confirm'],
        'modal confirm': def_rf_key_map['modal confirm'],
        'modal cancel': def_rf_key_map['modal cancel'],
    }

    ######################################
    #######  Selection and Action ########

    if act & nav_keys:
        print('Intersection of action and nav keys')
        print(act & nav_keys)
        print(f'{str(act)} detected in navigations keys')
        print('Please modify key_maps.py in addon directory')

        print('default keymap also conflicts with user navigation keys')
        bpy.ops.wm.url_open(url = "http://cgcookiemarkets.com/blender/forums/topic/custom-modal-hotkeys/")
    else:
        print(f'uneventfully added action keymap :{str(act)}')
        for val in act:
            add_to_dict(km_dict,'action', val, safety = False)
            add_to_dict(km_dict,'modal confirm', val, safety = False)

    if sel in nav_keys:
        print(f'{sel} for selection detected in navigations keys')
        #try default map
        if not def_map['select'] & nav_keys:
            sel = def_map['select']
            print('Default overrides does not conflict')
            for val in sel:
                add_to_dict(km_dict,'select', val, safety = False)

        else:
            print('Default select keymap also conflicts with user navigation keys')
            bpy.ops.wm.url_open(url = "http://cgcookiemarkets.com/blender/forums/topic/custom-modal-hotkeys/")
            km_dict = rtflow_def_default_keymap_generate()
            return(km_dict)
    else:
        print(f'uneventfully added select keymap :{str(sel)}')
        add_to_dict(km_dict,'select', sel, safety = False)
        add_to_dict(km_dict, 'modal cancel', sel, safety = True) #safety so that if select and action are same

    ######################################
    ######  Grab, Rotate and Scale  ######

    #direct keymaps to operators
    trans = set(find_kmi_by_idname('transform.translate', keymap = '3D View'))
    rot = set(find_kmi_by_idname('transform.rotate', keymap = '3D View'))
    scale = set(find_kmi_by_idname('transform.resize', keymap = '3D View'))

    #Transform Modal Map.  Maya has no operator keymap, just
    if 'Transform Modal Map' in keycon.keymaps:
        for kmi in keycon.keymaps['Transform Modal Map'].keymap_items:
            if kmi.propvalue == 'RESIZE' and not scale:
                scale = set(kmi_details(kmi))
            if kmi.propvalue == 'ROTATE' and not rot:
                rot = set(kmi_details(kmi))
            if kmi.propvalue == 'TRANSLATE' and not trans:
                trans = set(kmi_details(kmi))

    if not trans:
        print('Translate not found in operator keymap or Transform Modal Map')
        km_dict['translate'] = def_map['translate']    
    else:
        km_dict['translate'] = trans

    if not rot:
        print('default rotate used...no rotate found: ' + str(def_map['translate']))
        km_dict['rotate'] = def_map['rotate']
    else:
        km_dict['rotate'] = rot 


    if not scale:
        print('Scale not found in operator keymap or Transform Modal Map')
        km_dict['scale'] = def_map['scale']
    else:
        km_dict['scale'] = scale

    ##################################
    ######  Regular Operators  #######
    for key in ['up count', 'dn count', 'bridge','new','align','up shift','dn shift','smooth', 'snap cursor','view cursor','undo','mode', 'delete']:
        for val in def_map[key]:
            if not add_to_dict(km_dict, key, val, safety = True):
                print(f'left out {val} key for {key} operator')
                print('check your defaults')

    #navigation keys last, to avoid conflicts eg, Ctl + Wheel
    #center view on cursor is included in nav
    for kmi in keycon.keymaps['3D View'].keymap_items:
        if kmi.name in navigation_events and not add_to_dict(
            km_dict, 'navigate', kmi_details(kmi)
        ):
            print(f'Left out {kmi.name} navigation, collision with other key')

    #bug, WHEELOUTMOUSE and WHEELINMOUSE used in 3dview keymaap
    add_to_dict(km_dict,'navigate', 'WHEELDOWNMOUSE')
    add_to_dict(km_dict,'navigate', 'WHEELUPMOUSE')

    return km_dict