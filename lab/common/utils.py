from medicallab.models import Branch
def has_access_to(user, branch_id):
    if user.is_employer():
        return branch_id == user.branch.id
    elif user.is_lab_owner():
        try:
            user.lab.branches.get(pk=branch_id)
            return True
        except Branch.DoesNotExist:
            return False