# Sometimes it's a README fix, or something like that - which isn't relevant for
# including in a project's CHANGELOG for example
declared_trivial = github.pr_title.include? '#trivial'
wip = github.pr_title.include? '[WIP]'
added_and_modified_files = git.added_files + git.modified_files

warn('Big PR') if git.lines_of_code > 500

fail("PR not ready for review yet.") if wip

fail('Python debugger left in code', :sticky => true) if `egrep -r 'import i*pdb|pdb.set_trace' example/`.length > 1

# Inline comment PEP8 errors
if added_and_modified_files.include?('*.py')
  pep8.base_dir = 'bdd-trello-sync'
  pep8.config_file = 'setup.cfg'
  pep8.lint use_inline_comments: true
end

# Warn about new todos added to the code
todoist.warn_for_todos

# Ensure no merge commits
if git.commits.any? { |c| c.message =~ /^Merge branch/ }
  fail('Please rebase to get rid of the merge commits in this PR')
end

# Highlight api update if any change include view or serializers files
view_changes = added_and_modified_files.include?("*views*")
# serializer_changes = added_and_modified_files.include?("*serializers*")
# apidoc_changes = added_and_modified_files.include?("*apidoc.md*")
# postman_changes = added_and_modified_files.include?("*postman-collection.json*")

# if (view_changes or serializer_changes) and not (apidoc_changes and postman_changes)
#   warn('You make changes to the API without editing the documentation/postman collection.')
# end

# Ensure entry in changelog if PR is not trivial
# if !added_and_modified_files.include?("CHANGELOG.md") && !declared_trivial
#   fail("Please include a CHANGELOG entry.", sticky: false)
# end

# Analyse only the PR Diff
github.dismiss_out_of_range_messages
