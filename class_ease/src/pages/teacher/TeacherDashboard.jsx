import TeacherPanel from "../../components/TeachPanel";
import "../../styles/TeacherDashboard.css";
import "../../styles/Dashboard.css";
import TeacherHeader from "../../components/TeachHeader";

/**
 * TeacherDashboard component
 * @component
 * @return {component} TeacherDashboard
 * @example
 * return <TeacherDashboard />
 */
const TeacherDashboard = () => {
  return (
    <div className="min-h-screen flex flex-col">
      {/* Top Header */}
      <TeacherHeader />

      {/* Main content area: Sidebar + Content */}
      <div className="flex flex-1">
        {/* Sidebar */}
          <TeacherPanel />
        {/* Main Dashboard Content */}
        <main className="flex-1 p-6 bg-gray-100 overflow-scroll">
          {/* Teacher Stats */}
          <section className="mb-8">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="bg-white p-4 rounded shadow">
                <h3 className="text-lg font-semibold text-gray-700">Total Students</h3>
                <p className="text-2xl font-bold text-gray-900">30</p>
              </div>
              <div className="bg-white p-4 rounded shadow">
                <h3 className="text-lg font-semibold text-gray-700">Pending Assignments</h3>
                <p className="text-2xl font-bold text-gray-900">5 To Grade</p>
              </div>
            </div>
          </section>

          {/* Teacher Students Section */}
          <section>
            <h3 className="text-xl font-semibold text-gray-800 mb-4">My Students</h3>
            <div className="overflow-x-auto bg-white rounded shadow">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">ID</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Name</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Grade</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Score</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Action</th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  <tr>
                    <td className="px-6 py-4 whitespace-nowrap">1234</td>
                    <td className="px-6 py-4 whitespace-nowrap">John Doe</td>
                    <td className="px-6 py-4 whitespace-nowrap">Grade 10</td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <input
                        type="number"
                        defaultValue="85"
                        className="w-20 p-1 border border-gray-300 rounded"
                      />
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <button className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors">
                        Update
                      </button>
                    </td>
                  </tr>
                  <tr>
                    <td className="px-6 py-4 whitespace-nowrap">5678</td>
                    <td className="px-6 py-4 whitespace-nowrap">Jane Smith</td>
                    <td className="px-6 py-4 whitespace-nowrap">Grade 10</td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <input
                        type="number"
                        defaultValue="90"
                        className="w-20 p-1 border border-gray-300 rounded"
                      />
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <button className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors">
                        Update
                      </button>
                    </td>
                  </tr>
                  {/* Additional rows as needed */}
                </tbody>
              </table>
            </div>
          </section>
        </main>
      </div>
    </div>
  );
};

export default TeacherDashboard;
