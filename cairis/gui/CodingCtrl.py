#  Unless required by applicable law or agreed to in writing,
#  software distributed under the License is distributed on an
#  "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
#  KIND, either express or implied.  See the License for the
#  specific language governing permissions and limitations
#  under the License.

import wx
from cairis.core.armid import *
from CodingTextCtrl import CodingTextCtrl
from CodeMarginCtrl import CodeMarginCtrl

__author__ = 'Shamal Faily'

class CodingCtrl(wx.SplitterWindow):
  def __init__(self,parent, winId):
    wx.SplitterWindow.__init__(self,parent,winId)
    self.SetMinimumPaneSize(500)

    self.txtCtrl = CodingTextCtrl(self,winId)
    marginCtrl = CodeMarginCtrl(self,-1)
    marginCtrl.addCode('test category')
    self.SplitVertically(self.txtCtrl,marginCtrl)

  def SetValue(self,v):
    return self.txtCtrl.SetValue(v)

  def setCodes(self,cs):
    self.txtCtrl.setCodes(cs)

  def setMemos(self,ms):
    self.txtCtrl.setMemos(ms)

