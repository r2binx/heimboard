import sys
from dataclasses import dataclass
from typing import List, Tuple, Union, Dict
from xml.dom import minidom

import libvirt
from libvirt import virConnect, virDomain


class DomainState:
    # values from libvirt binding
    # VIR_DOMAIN_NOSTATE = 0
    # VIR_DOMAIN_RUNNING = 1
    # VIR_DOMAIN_BLOCKED = 2
    # VIR_DOMAIN_PAUSED = 3
    # VIR_DOMAIN_SHUTDOWN = 4
    # VIR_DOMAIN_SHUTOFF = 5
    # VIR_DOMAIN_CRASHED = 6
    # VIR_DOMAIN_PMSUSPENDED = 7

    state = {
        0: "no_state",
        1: "running",
        2: "blocked",
        3: "paused",
        4: "shutdown",
        5: "shutoff",
        6: "crashed",
        7: "suspended"
    }

    @staticmethod
    def get_state(state_int: int) -> str:
        state_str = DomainState.state.get(state_int)
        if state_str is None:
            return "no_state_found"
        else:
            return state_str


@dataclass
class State:
    name: str
    status: Dict[str, Union[str, bool]]


def inactive_domain(domain: str) -> State:
    return State(domain, {
        "success": False,
        "message": "Domain is not running"
    })


def shutdown_vm(domain: virDomain) -> bool:
    return True if domain.shutdown() == 0 else False


def destroy_vm(domain: virDomain) -> bool:
    return True if domain.destroy() == 0 else False


def pause_vm(domain: virDomain) -> bool:
    return True if domain.suspend() == 0 else False


def resume_vm(domain: virDomain) -> bool:
    return True if domain.resume() == 0 else False


class KVM:
    conn: virConnect

    def __init__(self):
        try:
            self.conn = libvirt.open("qemu:///system")
            if not self.conn:
                raise SystemExit("Failed to open connection to qemu:///system")
            else:
                print('Opened connection to the hypervisor')
        except libvirt.libvirtError:
            print('Failed to open connection to the hypervisor')
            sys.exit(1)

    def is_active(self):
        try:
            active_domains = self.get_active()

            if len(active_domains) > 0:
                return True
            else:
                return False

        except libvirt.libvirtError:
            print('Failed to get active domains')

    def get_active(self) -> List[Tuple[str, str]]:
        active_domains = list()
        try:
            if self.conn.numOfDomains() != 0:
                for d in self.conn.listAllDomains():
                    active = True if d.isActive() == 1 else False
                    if active:
                        name = d.name()
                        state = DomainState.get_state(d.state()[0])
                        active_domains.append((name, state))

            return active_domains

        except libvirt.libvirtError:
            print('Failed to find active domains')

        return active_domains

    def get_domain_running(self, domain) -> bool:
        try:
            active_domains = self.get_active()

            for active in active_domains:
                name = active[0]
                state = active[1]
                if name == domain and state == "running":
                    return True

        except libvirt.libvirtError:
            print('Failed to find active domains')

        return False

    def get_vms(self) -> List[Dict[str, any]]:
        try:
            vm_list = []
            for d in self.conn.listAllDomains():
                doc = minidom.parseString(d.XMLDesc())
                mem_editable = True if len(
                    doc.getElementsByTagName("memballoon")) > 0 else False

                info = {
                    "name": d.name(),
                    "UUID": d.UUIDString(),
                    "state": DomainState.get_state(d.state()[0]),
                    "mem_modifiable": mem_editable,
                    "max_memory": d.maxMemory()
                }

                if d.isActive():
                    info["current_memory"] = self.get_active_memory(
                        d.name()).status['message']

                vm_list.append(info)

            return vm_list

        except libvirt.libvirtError:
            print('Failed to get VMs')
            sys.exit(1)

    def boot_vm(self, domain: str) -> State:
        try:
            dom = self.conn.lookupByName(domain)
            success = True if dom.create() == 0 else False

            if success:
                return State(domain, {
                    "success": success,
                    "message": "Boot successful"
                })
            else:
                return State(domain, {
                    "success": success,
                    "message": "Failed to boot"
                })

        except libvirt.libvirtError:
            print(f"Failed to boot domain: {domain}")
            sys.exit(1)

    def change_vm_state(self, domain: str, state: str) -> State:
        try:
            success = False
            dom = self.get_active_domain(domain)
            if dom is not None:
                if state == 'shutdown' or state == 'stop':
                    success = shutdown_vm(dom)
                elif state == 'destroy':
                    success = destroy_vm(dom)
                elif state == 'pause' or state == 'suspend':
                    success = pause_vm(dom)
                elif state == 'resume':
                    success = resume_vm(dom)
                else:
                    return State(domain, {
                        "success": False,
                        "message": "Invalid state"
                    })
                if not success:
                    return State(domain, {
                        "success": success,
                        "message": f"Failed to change state: {state}"
                    })
                else:
                    return State(domain, {
                        "success": success,
                        "message": f"Successfully changed state to: {state}"
                    })
            else:
                return inactive_domain(domain)

        except libvirt.libvirtError:
            print('Failed to find active domains')
            sys.exit(1)

    def set_active_memory(self, domain: str, size: int) -> State:
        try:
            dom = self.get_active_domain(domain)
            if dom is not None:
                success = True if dom.setMemory(size) == 0 else False

                if success:
                    return State(
                        domain, {
                            "success": success,
                            "message": "Memory set to {}KiB".format(size)
                        })
                else:
                    return State(
                        domain, {
                            "success": success,
                            "message": "Failed setting memory to {}KiB".format(size)
                        })

            else:
                return inactive_domain(domain)

        except libvirt.libvirtError:
            print('Failed to set active memory')
            sys.exit(1)

    def get_active_domain(self, domain: str) -> Union[virDomain, None]:
        try:
            dom = self.conn.lookupByName(domain)
            if dom.isActive():
                return dom
            else:
                return None
        except libvirt.libvirtError:
            print('Failed to find active domains')

    def get_active_memory(self, domain: str) -> State:
        try:
            dom = self.conn.lookupByName(domain)
            if dom.isActive():
                mem = dom.memoryStats()

                return State(domain, {
                    "success": True,
                    "message": mem.get("actual")
                })

            else:
                return inactive_domain(domain)

        except libvirt.libvirtError:
            print('Failed to get active memory')
            sys.exit(1)

    def get_vm_info(self, domain: str) -> State:
        try:
            dom = self.conn.lookupByName(domain)
            if dom:
                state = DomainState.get_state(dom.state()[0])
                doc = minidom.parseString(dom.XMLDesc())
                mem_editable = True if len(
                    doc.getElementsByTagName("memballoon")) > 0 else False

                if dom.isActive():
                    mem = self.get_active_memory(domain).status["message"]

                    return State(
                        domain, {
                            "success": True,
                            "name": domain,
                            "state": state,
                            "mem_modifiable": mem_editable,
                            "memory": mem
                        })
                else:
                    return State(
                        domain, {
                            "success": True,
                            "name": domain,
                            "state": state,
                            "mem_modifiable": mem_editable,
                            "max_memory": dom.maxMemory()
                        })
            else:
                return State(
                    domain, {
                        "success": False,
                        "message": "Failed to get info for domain: " + domain
                    })

        except libvirt.libvirtError:
            print('Failed to get vm stats')
            sys.exit(1)

    def is_kvm_idle(self) -> bool:
        return not self.is_active()


if not __name__ == "__main__":
    print("kvm.py is imported")
else:
    kvm_controller = KVM()
    print(kvm_controller.get_vms())
