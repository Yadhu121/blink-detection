using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Http;
using System.Diagnostics;

namespace AlzermersDetection.Controllers
{
    public class HomeController : Controller
    {
        static int BlinkBpm = 0;
        static string BlinkLevel = "Waiting...";

        public IActionResult Index()
        {
            return View();
        }
        [HttpPost]
        public IActionResult StartBlink(string name, int age, string gender)
        {
            Console.WriteLine($"User: {name}, {age}, {gender}");

            string pythonPath = Path.Combine(Directory.GetCurrentDirectory(), "venv/bin/python");
            string scriptPath = Path.Combine(Directory.GetCurrentDirectory(), "Python/main.py");

            Process.Start(new ProcessStartInfo
            {
                FileName = pythonPath,
                Arguments = scriptPath,
                UseShellExecute = false,
                CreateNoWindow = true
            });

            return RedirectToAction("BlinkResult");
        }

        [HttpPost]
        [Route("Home/ReceiveBlink")]
        public IActionResult ReceiveBlink([FromBody] BlinkDto dto)
        {
            Console.WriteLine(">>> ReceiveBlink HIT <<<");
            Console.WriteLine($"Blink: {dto.Bpm}, {dto.Level}");

            BlinkBpm = dto.Bpm;
            BlinkLevel = dto.Level;

        return Ok();
        }

        public IActionResult BlinkResult()
        {
            ViewBag.Bpm = BlinkBpm;
            ViewBag.Level = BlinkLevel;
            return View();
        }

    public class BlinkDto
    {
        public int Bpm { get; set; }
        public string Level { get; set; }
    }
}
}