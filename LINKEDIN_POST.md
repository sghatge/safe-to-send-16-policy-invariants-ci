Safe to Send · Ep 16 — The pull request that looked reasonable

PR #42: "Speed up Black Friday: let the agent send small campaigns and run cleanup scripts."

Four lines of policy changed. Busy reviewers. It looks fine.

My CI said otherwise, in under a second:
❌ INV-04: Every send needs a human (policy now says 'allow')
❌ INV-05: Sends above 100,000 need two humans (now just one)
❌ INV-07: Server-side scripts never execute for real (now they do)

The trick is writing your non-negotiables once, as invariants: a test call plus the decisions you'll accept. Eight of them cover most of what scares me about agents in Adobe Campaign.

Then every policy change, however small, gets checked against all eight before it can merge.

Ten lines of GitHub Actions. It's the cheapest governance you'll ever add.

Repo: https://github.com/sghatge/safe-to-send-16-policy-invariants-ci

#SafeToSend #CICD #GitHubActions #AIGovernance
