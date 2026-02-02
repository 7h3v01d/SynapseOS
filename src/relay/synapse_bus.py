# synapse_bus.py
# Internal message bus for routing events between cognitive modules

class SynapseRelay:
    def __init__(self):
        # Registered modules (services)
        self.modules = {}

    def register(self, name, module):
        """
        Register a module (microservice) to the message bus
        """
        if name in self.modules:
            raise ValueError(f"Module '{name}' is already registered.")
        self.modules[name] = module
        print(f"[SynapseRelay] Registered module: {name}")

    def send(self, target_module, method_name, *args, **kwargs):
        """
        Send a message to a target module by invoking a method on it.
        """
        module = self.modules.get(target_module)
        if not module:
            raise ValueError(f"Module '{target_module}' is not registered.")

        method = getattr(module, method_name, None)
        if not method:
            raise AttributeError(f"'{target_module}' has no method '{method_name}'")

        print(f"[SynapseRelay] Dispatching: {target_module}.{method_name}()")
        return method(*args, **kwargs)

    def broadcast(self, method_name, *args, **kwargs):
        """
        Send the same method call to all modules.
        """
        results = {}
        for name, module in self.modules.items():
            method = getattr(module, method_name, None)
            if callable(method):
                print(f"[SynapseRelay] Broadcasting to: {name}.{method_name}()")
                results[name] = method(*args, **kwargs)
        return results
