using System.IO;
using System.Web;
using System.Web.Mvc;

namespace soundlens.Controllers
{
    public class HomeController : Controller
    {
        // GET: Home
        [HttpGet]
        public ActionResult Index()
        {
            return View();
        }

        [HttpPost]
        public ActionResult Index(string url)
        {
            return View();
        }

        public ActionResult About()
        {
            return View();
        }

        public async System.Threading.Tasks.Task<ActionResult> sendImg(string imgUrl)
        {
            

            return View();
        }

        //public ActionResult FileUpload(HttpPostedFileBase file)
        //{
        //    if (file != null)
        //    {
        //        string pic = System.IO.Path.GetFileName(file.FileName);
        //        string path = System.IO.Path.Combine(
        //                               Server.MapPath("~/images/profile"), pic);
        //        // file is uploaded
        //        file.SaveAs(path);

        //        // save the image path path to the database or you can send image
        //        // directly to database
        //        // in-case if you want to store byte[] ie. for DB
        //        using (MemoryStream ms = new MemoryStream())
        //        {
        //            file.InputStream.CopyTo(ms);
        //            byte[] array = ms.GetBuffer();
        //        }

        //    }
        //    // after successfully uploading redirect the user
        //    return RedirectToAction("actionname", "controller name");
        // }
    }
}