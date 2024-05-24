import unreal

# Get the level editor subsystem
level_editor_subsystem = unreal.LevelEditorSubsystem()

# Define the actor class and location
actor_class = unreal.StaticMeshActor
location = unreal.Vector(0.0, 0.0, 0.0)

# Spawn the actor in the level
actor = level_editor_subsystem.spawn_actor_from_class(actor_class, location)