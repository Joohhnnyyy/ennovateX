import { Metadata } from 'next'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Users, MessageSquare, Share2, GitBranch, Calendar, FileText, Video, Shield } from 'lucide-react'
import Link from 'next/link'

export const metadata: Metadata = {
  title: 'Team Collaboration | Ennovatex AI Platform',
  description: 'Powerful collaboration tools for seamless teamwork. Real-time editing, version control, and integrated communication.',
}

export default function TeamCollaborationPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      {/* Hero Section */}
      <div className="relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-r from-purple-500/10 to-pink-500/10" />
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-20 pb-16">
          <div className="text-center">
            <Badge variant="outline" className="mb-4 border-purple-500/50 text-purple-300">
              Team Collaboration
            </Badge>
            <h1 className="text-4xl md:text-6xl font-bold text-white mb-6">
              Work Together,
              <span className="bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">
                {' '}Achieve More
              </span>
            </h1>
            <p className="text-xl text-gray-300 mb-8 max-w-3xl mx-auto">
              Seamless collaboration tools that bring your team together. Real-time editing, 
              version control, and integrated communication for maximum productivity.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Button size="lg" className="bg-purple-600 hover:bg-purple-700">
                Start Collaborating
              </Button>
              <Button size="lg" variant="outline" className="border-purple-500/50 text-purple-300 hover:bg-purple-500/10">
                View Demo
              </Button>
            </div>
          </div>
        </div>
      </div>

      {/* Collaboration Features */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="text-center mb-16">
          <h2 className="text-3xl font-bold text-white mb-4">Collaboration Features</h2>
          <p className="text-gray-400 max-w-2xl mx-auto">
            Everything your team needs to work together effectively
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          <Card className="bg-slate-800/50 border-slate-700">
            <CardHeader>
              <MessageSquare className="h-8 w-8 text-purple-400 mb-2" />
              <CardTitle className="text-white">Real-time Chat</CardTitle>
              <CardDescription className="text-gray-400">
                Instant messaging with file sharing and emoji reactions
              </CardDescription>
            </CardHeader>
            <CardContent>
              <ul className="space-y-2 text-sm text-gray-300">
                <li>• Thread conversations</li>
                <li>• File attachments</li>
                <li>• @mentions and notifications</li>
                <li>• Message history search</li>
              </ul>
            </CardContent>
          </Card>

          <Card className="bg-slate-800/50 border-slate-700">
            <CardHeader>
              <FileText className="h-8 w-8 text-blue-400 mb-2" />
              <CardTitle className="text-white">Document Collaboration</CardTitle>
              <CardDescription className="text-gray-400">
                Real-time document editing with version control
              </CardDescription>
            </CardHeader>
            <CardContent>
              <ul className="space-y-2 text-sm text-gray-300">
                <li>• Live cursor tracking</li>
                <li>• Comment and suggestion mode</li>
                <li>• Auto-save and sync</li>
                <li>• Revision history</li>
              </ul>
            </CardContent>
          </Card>

          <Card className="bg-slate-800/50 border-slate-700">
            <CardHeader>
              <Video className="h-8 w-8 text-green-400 mb-2" />
              <CardTitle className="text-white">Video Conferencing</CardTitle>
              <CardDescription className="text-gray-400">
                HD video calls with screen sharing and recording
              </CardDescription>
            </CardHeader>
            <CardContent>
              <ul className="space-y-2 text-sm text-gray-300">
                <li>• Up to 100 participants</li>
                <li>• Screen sharing</li>
                <li>• Meeting recording</li>
                <li>• Virtual backgrounds</li>
              </ul>
            </CardContent>
          </Card>

          <Card className="bg-slate-800/50 border-slate-700">
            <CardHeader>
              <GitBranch className="h-8 w-8 text-orange-400 mb-2" />
              <CardTitle className="text-white">Version Control</CardTitle>
              <CardDescription className="text-gray-400">
                Track changes and manage project versions
              </CardDescription>
            </CardHeader>
            <CardContent>
              <ul className="space-y-2 text-sm text-gray-300">
                <li>• Git integration</li>
                <li>• Branch management</li>
                <li>• Merge conflict resolution</li>
                <li>• Code review tools</li>
              </ul>
            </CardContent>
          </Card>

          <Card className="bg-slate-800/50 border-slate-700">
            <CardHeader>
              <Calendar className="h-8 w-8 text-pink-400 mb-2" />
              <CardTitle className="text-white">Project Planning</CardTitle>
              <CardDescription className="text-gray-400">
                Kanban boards, timelines, and milestone tracking
              </CardDescription>
            </CardHeader>
            <CardContent>
              <ul className="space-y-2 text-sm text-gray-300">
                <li>• Kanban boards</li>
                <li>• Gantt charts</li>
                <li>• Sprint planning</li>
                <li>• Progress tracking</li>
              </ul>
            </CardContent>
          </Card>

          <Card className="bg-slate-800/50 border-slate-700">
            <CardHeader>
              <Share2 className="h-8 w-8 text-cyan-400 mb-2" />
              <CardTitle className="text-white">File Sharing</CardTitle>
              <CardDescription className="text-gray-400">
                Secure file sharing with permission controls
              </CardDescription>
            </CardHeader>
            <CardContent>
              <ul className="space-y-2 text-sm text-gray-300">
                <li>• Drag & drop uploads</li>
                <li>• Permission management</li>
                <li>• Link sharing</li>
                <li>• File versioning</li>
              </ul>
            </CardContent>
          </Card>
        </div>
      </div>

      {/* Team Management */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="bg-gradient-to-r from-purple-900/20 to-pink-900/20 rounded-2xl p-8 border border-purple-500/20">
          <div className="grid lg:grid-cols-2 gap-8 items-center">
            <div>
              <h3 className="text-2xl font-bold text-white mb-4">Team Management</h3>
              <p className="text-gray-300 mb-6">
                Organize your team with role-based permissions, workspace management, 
                and activity tracking.
              </p>
              <div className="space-y-4">
                <div className="flex items-center gap-3">
                  <Users className="h-5 w-5 text-purple-400" />
                  <span className="text-gray-300">Role-based access control</span>
                </div>
                <div className="flex items-center gap-3">
                  <Shield className="h-5 w-5 text-purple-400" />
                  <span className="text-gray-300">Workspace security</span>
                </div>
                <div className="flex items-center gap-3">
                  <Calendar className="h-5 w-5 text-purple-400" />
                  <span className="text-gray-300">Activity monitoring</span>
                </div>
              </div>
            </div>
            <div className="bg-slate-800/50 rounded-xl p-6 border border-slate-700">
              <h4 className="text-lg font-semibold text-white mb-4">Team Roles</h4>
              <div className="space-y-3">
                <div className="flex justify-between items-center">
                  <span className="text-gray-300">Admin</span>
                  <Badge variant="outline" className="border-red-500/50 text-red-300">Full Access</Badge>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-300">Editor</span>
                  <Badge variant="outline" className="border-blue-500/50 text-blue-300">Edit & Comment</Badge>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-300">Viewer</span>
                  <Badge variant="outline" className="border-green-500/50 text-green-300">View Only</Badge>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-300">Guest</span>
                  <Badge variant="outline" className="border-gray-500/50 text-gray-300">Limited Access</Badge>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Integration Ecosystem */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="text-center mb-12">
          <h3 className="text-2xl font-bold text-white mb-4">Integration Ecosystem</h3>
          <p className="text-gray-400 max-w-2xl mx-auto">
            Connect with your favorite tools and streamline your workflow
          </p>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-6">
          {[
            'Slack', 'Discord', 'Microsoft Teams', 'Zoom', 'GitHub', 'GitLab',
            'Jira', 'Trello', 'Asana', 'Notion', 'Figma', 'Adobe Creative'
          ].map((tool) => (
            <div key={tool} className="bg-slate-800/30 rounded-lg p-4 text-center border border-slate-700/50 hover:border-purple-500/50 transition-colors">
              <div className="h-8 w-8 bg-gradient-to-br from-purple-500 to-pink-500 rounded mx-auto mb-2" />
              <span className="text-sm text-gray-300">{tool}</span>
            </div>
          ))}
        </div>
      </div>

      {/* CTA Section */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="text-center">
          <h3 className="text-3xl font-bold text-white mb-4">
            Ready to Transform Your Team Collaboration?
          </h3>
          <p className="text-gray-400 mb-8 max-w-2xl mx-auto">
            Join thousands of teams already collaborating more effectively with our platform.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button size="lg" className="bg-purple-600 hover:bg-purple-700">
              Start Free Trial
            </Button>
            <Button size="lg" variant="outline" className="border-purple-500/50 text-purple-300 hover:bg-purple-500/10">
              <Link href="/contact">Contact Sales</Link>
            </Button>
          </div>
        </div>
      </div>
    </div>
  )
}