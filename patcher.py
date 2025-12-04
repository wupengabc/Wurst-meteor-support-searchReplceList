search_replace_list = [

# fabric.mod.json

('src/main/resources/fabric.mod.json', '"id": "wurst"', '"id": "wurst-meteor"'),

# GameRendererMixin

('src/main/java/net/wurstclient/mixin/GameRendererMixin.java', '\n\t@Redirect(\n\t\tat = @At(value = "INVOKE",\n\t\t\ttarget = "Lnet/minecraft/util/math/MathHelper;lerp(FFF)F",\n\t\t\tordinal = 0),\n\t\tmethod = "renderWorld(FJLnet/minecraft/client/util/math/MatrixStack;)V")\n\tprivate float wurstNauseaLerp(float delta, float start, float end)\n\t{\n\t\tif(!WurstClient.INSTANCE.getHax().antiWobbleHack.isEnabled())\n\t\t\treturn MathHelper.lerp(delta, start, end);\n\t\t\n\t\treturn 0;\n\t}\n\t', ''),

# ClientPlayerEntitiyMixin

('src/main/java/net/wurstclient/mixin/ClientPlayerEntityMixin.java', 'import net.wurstclient.events.IsPlayerInLavaListener.IsPlayerInLavaEvent;', ''),

('src/main/java/net/wurstclient/mixin/ClientPlayerEntityMixin.java', '\n\t@Override\n\tpublic boolean isInLava()\n\t{\n\t\tboolean inLava = super.isInLava();\n\t\tIsPlayerInLavaEvent event = new IsPlayerInLavaEvent(inLava);\n\t\tEventManager.fire(event);\n\t\t\n\t\treturn event.isInLava();\n\t}\n\t\n\t@Override\n\tpublic boolean isSpectator()\n\t{\n\t\treturn super.isSpectator()\n\t\t\t|| WurstClient.INSTANCE.getHax().freecamHack.isEnabled();\n\t}\n\t', ''),

# CameraMixin

('src/main/java/net/wurstclient/mixin/CameraMixin.java', 'import org.spongepowered.asm.mixin.injection.ModifyVariable;', ''),

('src/main/java/net/wurstclient/mixin/CameraMixin.java', 'import net.wurstclient.hacks.CameraDistanceHack;', ''),

('src/main/java/net/wurstclient/mixin/CameraMixin.java', '\n\t@ModifyVariable(at = @At("HEAD"),\n\t\tmethod = "clipToSpace(F)F",\n\t\targsOnly = true)\n\tprivate float changeClipToSpaceDistance(float desiredCameraDistance)\n\t{\n\t\tCameraDistanceHack cameraDistance =\n\t\t\tWurstClient.INSTANCE.getHax().cameraDistanceHack;\n\t\tif(cameraDistance.isEnabled())\n\t\t\treturn cameraDistance.getDistance();\n\t\t\n\t\treturn desiredCameraDistance;\n\t}\n\t', ''),

# BlockMixin

('src/main/java/net/wurstclient/mixin/BlockMixin.java', '\n\t\n\t@Inject(at = @At("HEAD"),\n\t\tmethod = "getVelocityMultiplier()F",\n\t\tcancellable = true)\n\tprivate void onGetVelocityMultiplier(CallbackInfoReturnable<Float> cir)\n\t{\n\t\tHackList hax = WurstClient.INSTANCE.getHax();\n\t\tif(hax == null || !hax.noSlowdownHack.isEnabled())\n\t\t\treturn;\n\t\t\n\t\tif(cir.getReturnValueF() < 1)\n\t\t\tcir.setReturnValue(1F);\n\t}', ''),

# FilterShulkerBulletSetting

('src/main/java/net/wurstclient/hacks/ProtectHack.java', 'FilterShulkerBulletSetting.genericCombat(false),', ''),

('src/main/java/net/wurstclient/hacks/KillauraLegitHack.java', 'FilterShulkerBulletSetting.genericCombat(false),', ''),

('src/main/java/net/wurstclient/hacks/AimAssistHack.java', 'FilterShulkerBulletSetting.genericCombat(false),', ''),

('src/main/java/net/wurstclient/settings/filterlists/EntityFilterList.java', 'FilterShulkerBulletSetting.genericCombat(false),', ''),

# Freecam

('src/main/java/net/wurstclient/hacks/FreecamHack.java', 'IsPlayerInLavaListener, CameraTransformViewBobbingListener,', 'PlayerMoveListener, CameraTransformViewBobbingListener,'),

('src/main/java/net/wurstclient/hacks/FreecamHack.java', 'EVENTS.add(IsPlayerInLavaListener.class, this);', 'EVENTS.add(PlayerMoveListener.class, this);'),

('src/main/java/net/wurstclient/hacks/FreecamHack.java', 'EVENTS.remove(IsPlayerInLavaListener.class, this);', 'EVENTS.remove(PlayerMoveListener.class, this);'),

('src/main/java/net/wurstclient/hacks/FreecamHack.java', '@Override\n\tpublic void onIsPlayerInLava(IsPlayerInLavaEvent event)\n\t{\n\t\tevent.setInLava(false);\n\t}', ''),             # Remove onIsPlayerInLava

('src/main/java/net/wurstclient/hacks/FreecamHack.java', 'GL11.glDisable(GL11.GL_BLEND);\n\t}\n}', 'GL11.glDisable(GL11.GL_BLEND);\n\t}\n\t@Override\n\tpublic void onPlayerMove() {}\n}'),  # Add  P.S. Not work BRO   PLEASE SELF FIX

]