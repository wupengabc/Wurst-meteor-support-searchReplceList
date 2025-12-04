import os
import re
import subprocess

ROOT = os.path.dirname(os.path.abspath(__file__))

def read(path):
    p = os.path.join(ROOT, path)
    with open(p, "r", encoding="utf-8") as f:
        return f.read()

def write(path, content):
    p = os.path.join(ROOT, path)
    with open(p, "w", encoding="utf-8") as f:
        f.write(content)

def replace_in_file(path, old, new):
    try:
        s = read(path)
    except FileNotFoundError:
        return False
    if old in s:
        s = s.replace(old, new)
        write(path, s)
        return True
    return False

def remove_block_regex(path, pattern):
    try:
        s = read(path)
    except FileNotFoundError:
        return False
    m = re.search(pattern, s, flags=re.S)
    if not m:
        return False
    s = s[:m.start()] + s[m.end():]
    write(path, s)
    return True

def apply_changes():
    changes = 0

    changes += bool(replace_in_file(
        "src/main/resources/fabric.mod.json",
        '"id": "wurst"',
        '"id": "wurst-meteor"'
    ))

    grm = "src/main/java/net/wurstclient/mixin/GameRendererMixin.java"
    changes += bool(replace_in_file(grm, (
        "\n\t@Redirect(\n\t\tat = @At(value = \"INVOKE\",\n\t\t\ttarget = \"Lnet/minecraft/util/math/MathHelper;lerp(FFF)F\",\n\t\t\tordinal = 0),\n\t\tmethod = \"renderWorld(FJLnet/minecraft/client/util/math/MatrixStack;)V\")\n\tprivate float wurstNauseaLerp(float delta, float start, float end)\n\t{\n\t\tif(!WurstClient.INSTANCE.getHax().antiWobbleHack.isEnabled())\n\t\t\treturn MathHelper.lerp(delta, start, end);\n\t\t\n\t\treturn 0;\n\t}\n\t"), ""))
    changes += bool(remove_block_regex(grm, r"@WrapOperation[\s\S]*?Mth;lerp\(FFF\)F[\s\S]*?return 0;[\s\S]*?\}"))

    cpe = "src/main/java/net/wurstclient/mixin/ClientPlayerEntityMixin.java"
    changes += bool(replace_in_file(cpe,
        "import net.wurstclient.events.IsPlayerInLavaListener.IsPlayerInLavaEvent;",
        ""))
    changes += bool(replace_in_file(cpe, (
        "\n\t@Override\n\tpublic boolean isInLava()\n\t{\n\t\tboolean inLava = super.isInLava();\n\t\tIsPlayerInLavaEvent event = new IsPlayerInLavaEvent(inLava);\n\t\tEventManager.fire(event);\n\t\t\n\t\treturn event.isInLava();\n\t}\n\t\n\t@Override\n\tpublic boolean isSpectator()\n\t{\n\t\treturn super.isSpectator()\n\t\t\t|| WurstClient.INSTANCE.getHax().freecamHack.isEnabled();\n\t}\n\t"), ""))

    cam = "src/main/java/net/wurstclient/mixin/CameraMixin.java"
    changes += bool(replace_in_file(cam,
        "import org.spongepowered.asm.mixin.injection.ModifyVariable;",
        ""))
    changes += bool(replace_in_file(cam,
        "import net.wurstclient.hacks.CameraDistanceHack;",
        ""))
    changes += bool(replace_in_file(cam, (
        "\n\t@ModifyVariable(at = @At(\"HEAD\"),\n\t\tmethod = \"clipToSpace(F)F\",\n\t\targsOnly = true)\n\tprivate float changeClipToSpaceDistance(float desiredCameraDistance)\n\t{\n\t\tCameraDistanceHack cameraDistance =\n\t\t\tWurstClient.INSTANCE.getHax().cameraDistanceHack;\n\t\tif(cameraDistance.isEnabled())\n\t\t\treturn cameraDistance.getDistance();\n\t\t\n\t\treturn desiredCameraDistance;\n\t}\n\t"), ""))
    changes += bool(remove_block_regex(cam, r"@ModifyVariable[\s\S]*?getMaxZoom\(F\)F[\s\S]*?return desiredCameraDistance;[\s\S]*?\}"))

    blk = "src/main/java/net/wurstclient/mixin/BlockMixin.java"
    changes += bool(replace_in_file(blk, (
        "\n\t\n\t@Inject(at = @At(\"HEAD\"),\n\t\tmethod = \"getVelocityMultiplier()F\",\n\t\tcancellable = true)\n\tprivate void onGetVelocityMultiplier(CallbackInfoReturnable<Float> cir)\n\t{\n\t\tHackList hax = WurstClient.INSTANCE.getHax();\n\t\tif(hax == null || !hax.noSlowdownHack.isEnabled())\n\t\t\treturn;\n\t\t\n\t\tif(cir.getReturnValueF() < 1)\n\t\t\tcir.setReturnValue(1F);\n\t}"), ""))
    changes += bool(remove_block_regex(blk, r"@Inject[\s\S]*?getSpeedFactor\(\)F[\s\S]*?cir\.setReturnValue\(1F\);[\s\S]*?\}"))
    changes += bool(replace_in_file(blk,
        "import net.wurstclient.WurstClient;", ""))
    changes += bool(replace_in_file(blk,
        "import net.wurstclient.hack.HackList;", ""))

    for p in [
        "src/main/java/net/wurstclient/hacks/ProtectHack.java",
        "src/main/java/net/wurstclient/hacks/KillauraLegitHack.java",
        "src/main/java/net/wurstclient/hacks/AimAssistHack.java",
        "src/main/java/net/wurstclient/settings/filterlists/EntityFilterList.java",
    ]:
        changes += bool(replace_in_file(p,
            "FilterShulkerBulletSetting.genericCombat(false),", ""))

    fh = "src/main/java/net/wurstclient/hacks/FreecamHack.java"
    changes += bool(replace_in_file(fh,
        "IsPlayerInLavaListener, CameraTransformViewBobbingListener,",
        "PlayerMoveListener, CameraTransformViewBobbingListener,"))
    changes += bool(replace_in_file(fh,
        "EVENTS.add(IsPlayerInLavaListener.class, this);",
        "EVENTS.add(PlayerMoveListener.class, this);"))
    changes += bool(replace_in_file(fh,
        "EVENTS.remove(IsPlayerInLavaListener.class, this);",
        "EVENTS.remove(PlayerMoveListener.class, this);"))
    changes += bool(replace_in_file(fh, (
        "\n\t@Override\n\tpublic void onIsPlayerInLava(IsPlayerInLavaEvent event)\n\t{\n\t\tevent.setInLava(false);\n\t}\n"), "\n\t@Override\n\tpublic void onPlayerMove()\n\t{}\n"))

    return changes

def compile_project():
    bat = os.path.join(ROOT, "gradlew.bat")
    cmd1 = [bat, "spotlessApply"]
    cmd2 = [bat, "build", "-x", "test"]
    subprocess.run(cmd1, cwd=ROOT, check=False)
    subprocess.run(cmd2, cwd=ROOT, check=True)

if __name__ == "__main__":
    c = apply_changes()
    compile_project()
    print("changes", c)
