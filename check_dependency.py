from github import Auth, Github

import private_config
import tools

auth = Auth.Token(private_config.token)

g = Github(auth=auth)
repo = g.get_repo("OCA/OpenUpgrade")

version = 14.0

# Get Opened PRs
_done_prs, opened_prs = tools._get_prs(repo, version)

# Get Done modules
module_coverage = tools._get_module_coverage(repo, version)


def module_ok(module_name):
    return module_coverage[module_name] in ["nothing_to_do", "done"]


for module_name, pr_number in opened_prs.items():
    manifest = tools._get_manifest_module(repo, version, module_name)
    if not manifest:
        # the module disappeared in the new version
        continue

    depends = manifest.get("depends")
    pr = repo.get_pull(pr_number)

    current_labels = [x.name for x in pr.labels]
    new_labels = current_labels.copy()

    message = f"PR #{pr_number} for {module_name}:"
    if all([module_ok(x) for x in depends]):
        # all dependencies are OK, mark the PR as OK.
        label_to_remove = "Blocked by dependency"
        label_to_add = "Dependency OK"
    else:
        # mark the PR as blocked
        label_to_remove = "Dependency OK"
        label_to_add = "Blocked by dependency"

    if label_to_remove in new_labels:
        message += f" Remove '{label_to_remove}'"
        new_labels.remove(label_to_remove)

    if label_to_add not in new_labels:
        message += f" Set '{label_to_add}'"
        new_labels.append(label_to_add)

    if new_labels != current_labels:
        tools._logger.info(message)
        pr.set_labels(*new_labels)
